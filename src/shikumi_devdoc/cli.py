"""Command-line interface for shikumi-devdoc."""

from __future__ import annotations

import argparse
import importlib
import inspect
from pathlib import Path
import sys
import tomllib
from types import ModuleType
from typing import Sequence

from shikumi import Diagnostic

from shikumi_devdoc.context import Context, ContextError
from shikumi_devdoc.norms.changelog import changelog_system
from shikumi_devdoc.norms.common import CanonicalSource
from shikumi_devdoc.norms.document import document
from shikumi_devdoc.norms.vocabulary import vocabulary_system
from shikumi_devdoc.realizers import (
    ChangelogMarkdownRealizer,
    DocumentMarkdownRealizer,
    GlossaryMarkdownRealizer,
    PythonReferenceModuleRealizer,
    TranslationSourceRealizer,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shikumi-devdoc")
    subparsers = parser.add_subparsers(dest="command", required=True)

    terms = subparsers.add_parser(
        "terms",
        help="generate a human-readable Python term-reference module from a vocabulary source",
    )
    terms.add_argument(
        "module",
        help="dotted import path of the canonical vocabulary module",
    )
    terms.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="path of the generated Python module",
    )

    render = subparsers.add_parser(
        "render",
        help="validate a canonical source and render an intermediate Markdown document",
    )
    render.add_argument(
        "kind",
        choices=("document", "glossary", "changelog"),
        help="kind of canonical source to render",
    )
    render.add_argument(
        "module",
        help="dotted import path of the canonical source module",
    )
    render.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="path of the generated Markdown file",
    )
    render.add_argument(
        "--context",
        help="JSON object containing the external-context snapshot for this rendering",
    )
    render.add_argument(
        "--notice",
        type=Path,
        help="explicit TOML notice file whose [notice].content is embedded as a Markdown comment",
    )
    render.add_argument(
        "--translation-source",
        action="store_true",
        help="embed translation metadata such as preserve-spelling terms in the Markdown source",
    )
    return parser


def _subject_name(subject: object | None) -> str | None:
    if subject is None:
        return None
    if isinstance(subject, ModuleType):
        return getattr(subject, "__name__", None)
    module = getattr(subject, "__module__", None)
    qualname = getattr(subject, "__qualname__", None)
    if isinstance(module, str) and isinstance(qualname, str):
        return f"{module}.{qualname}"
    name = getattr(subject, "__name__", None)
    return name if isinstance(name, str) else None


def _source_location(subject: object | None) -> str | None:
    if subject is None:
        return None

    path: str | None = None
    line: int | None = None
    try:
        if isinstance(subject, ModuleType):
            raw = getattr(subject, "__file__", None)
            path = raw if isinstance(raw, str) else None
        else:
            path = inspect.getsourcefile(subject)
            if path is not None:
                _, line = inspect.getsourcelines(subject)
    except (OSError, TypeError):
        pass

    if path is None:
        return None
    source = Path(path).resolve()
    try:
        rendered = source.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        rendered = source.as_posix()
    return f"{rendered}:{line}" if line is not None else rendered


def _format_diagnostic(diagnostic: Diagnostic) -> str:
    severity = diagnostic.severity.value
    code = f" [{diagnostic.code}]" if diagnostic.code else ""
    location = _source_location(diagnostic.subject)
    subject = _subject_name(diagnostic.subject)

    header = f"{severity}{code}"
    if location:
        header += f" {location}"
    rows = [header]
    if subject:
        rows.append(f"  {subject}")
    rows.append(f"  {diagnostic.message}")
    return "\n".join(rows)


def _print_diagnostics(diagnostics) -> None:
    for index, diagnostic in enumerate(diagnostics):
        if index:
            print(file=sys.stderr)
        print(_format_diagnostic(diagnostic), file=sys.stderr)


def _render_terms(module_name: str, output: Path) -> int:
    module = importlib.import_module(module_name)
    result = vocabulary_system.validate(module, placement=())
    if result.diagnostics:
        _print_diagnostics(result.diagnostics)
    if not result.is_valid:
        return 1

    realizer = PythonReferenceModuleRealizer(module_name)
    check = realizer.check(result.view)
    if check.diagnostics:
        _print_diagnostics(check.diagnostics)
    if not check.is_realizable:
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(realizer.realize(result.view), encoding="utf-8")
    print(output)
    return 0


def _canonical_source(module: object) -> str:
    raw = getattr(module, "__file__", None)
    if not isinstance(raw, str):
        return getattr(module, "__name__", "<unknown>")
    path = Path(raw).resolve()
    try:
        return path.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _load_notice(path: Path | None, canonical_source: str) -> str | None:
    if path is None:
        return None
    with path.open("rb") as stream:
        config = tomllib.load(stream)
    notice = config.get("notice")
    if not isinstance(notice, dict) or not isinstance(notice.get("content"), str):
        raise ValueError(f"notice TOML requires [notice].content: {path}")
    return notice["content"].strip().replace(
        "{canonical_source}",
        canonical_source,
    )


def _canonical_source_from_view(view, fallback: object) -> str:
    values = [
        value
        for item in view.entities
        for value in item.values(CanonicalSource)
    ]
    if len(values) == 1:
        return values[0]
    return _canonical_source(fallback)


def _render_markdown(
    kind: str,
    module_name: str,
    output: Path,
    context_json: str | None,
    notice_path: Path | None,
    translation_source: bool,
) -> int:
    importlib.invalidate_caches()
    module = importlib.import_module(module_name)
    context = Context.from_json(context_json) if context_json is not None else Context({})

    if kind == "document":
        system = document
        realizer_type = DocumentMarkdownRealizer
    elif kind == "glossary":
        system = vocabulary_system
        realizer_type = GlossaryMarkdownRealizer
    elif kind == "changelog":
        system = changelog_system
        realizer_type = ChangelogMarkdownRealizer
    else:  # pragma: no cover - argparse constrains this value
        raise ValueError(f"unknown render kind: {kind}")

    result = system.validate(module, placement=())
    if result.diagnostics:
        _print_diagnostics(result.diagnostics)
    if not result.is_valid:
        return 1

    canonical_source = _canonical_source_from_view(result.view, module)
    header_comment = _load_notice(notice_path, canonical_source)
    realizer = realizer_type(context, header_comment=header_comment)
    if translation_source:
        realizer = TranslationSourceRealizer(realizer)

    check = realizer.check(result.view)
    if check.diagnostics:
        _print_diagnostics(check.diagnostics)
    if not check.is_realizable:
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(realizer.realize(result.view), encoding="utf-8")
    print(output)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "terms":
            return _render_terms(args.module, args.output)
        if args.command == "render":
            return _render_markdown(
                args.kind,
                args.module,
                args.output,
                args.context,
                args.notice,
                args.translation_source,
            )
    except (OSError, ValueError, ContextError) as exc:
        print(exc, file=sys.stderr)
        return 1
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
