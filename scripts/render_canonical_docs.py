from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_DOCUMENTS = ROOT / "devdocs/canonical_documents"
CONTEXT_FILE = ROOT / "devdocs/config/context.json"
NOTICE_FILE = ROOT / "devdocs/config/notice.toml"


def _run_cli(*args: str | Path) -> None:
    command = [sys.executable, "-m", "shikumi_devdoc.cli", *(str(arg) for arg in args)]
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def _render(output: Path) -> None:
    context = CONTEXT_FILE.read_text(encoding="utf-8")

    _run_cli(
        "render",
        "glossary",
        "devdocs.canonical_sources.vocabulary.canonical",
        "-o",
        output / "GLOSSARY.md",
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "document",
        "devdocs.canonical_sources.readme.canonical",
        "-o",
        output,
        "--context",
        context,
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "document",
        "devdocs.canonical_sources.authoring_guide",
        "-o",
        output / "authoring_guide",
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "index",
        "devdocs.canonical_sources.authoring_guide",
        "-o",
        output / "authoring_guide",
        "--index-title",
        "shikumi-devdoc Authoring Guide",
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "document",
        "devdocs.canonical_sources.workspace.canonical",
        "-o",
        output / "devdocs",
        "--notice",
        NOTICE_FILE,
    )
    _run_cli(
        "render",
        "document",
        "devdocs.canonical_sources.status.canonical",
        "-o",
        output,
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "document",
        "devdocs.canonical_sources.changelog.canonical",
        "-o",
        output / "changelog",
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "document",
        "devdocs.canonical_sources.specification",
        "-o",
        output / "specification",
        "--context",
        context,
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "index",
        "devdocs.canonical_sources.specification",
        "-o",
        output / "specification",
        "--context",
        context,
        "--index-title",
        "shikumi-devdoc Specification",
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "document",
        "devdocs.canonical_sources.api_reference",
        "-o",
        output / "api",
        "--context",
        context,
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )
    _run_cli(
        "render",
        "index",
        "devdocs.canonical_sources.api_reference",
        "-o",
        output / "api",
        "--context",
        context,
        "--index-title",
        "shikumi-devdoc API Reference",
        "--notice",
        NOTICE_FILE,
        "--translation-source",
    )


def _files(root: Path) -> dict[Path, bytes]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _check(generated: Path) -> None:
    expected = _files(CANONICAL_DOCUMENTS)
    actual = _files(generated)

    missing = sorted(expected.keys() - actual.keys())
    extra = sorted(actual.keys() - expected.keys())
    changed = sorted(path for path in expected.keys() & actual.keys() if expected[path] != actual[path])

    if not (missing or extra or changed):
        print("canonical documents are up to date")
        return

    if missing:
        print("missing generated files:", file=sys.stderr)
        for path in missing:
            print(f"  {path}", file=sys.stderr)
    if extra:
        print("unexpected generated files:", file=sys.stderr)
        for path in extra:
            print(f"  {path}", file=sys.stderr)
    if changed:
        print("out-of-date canonical documents:", file=sys.stderr)
        for path in changed:
            print(f"  {path}", file=sys.stderr)

    raise SystemExit("canonical documents are not up to date; regenerate them")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render this repository's canonical documents.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify committed canonical documents match freshly rendered output.",
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="shikumi-devdoc-canonical-") as temp:
        generated = Path(temp) / "canonical_documents"
        generated.mkdir()
        _render(generated)

        if args.check:
            _check(generated)
            return

        if CANONICAL_DOCUMENTS.exists():
            shutil.rmtree(CANONICAL_DOCUMENTS)
        shutil.copytree(generated, CANONICAL_DOCUMENTS)
        print(f"rendered canonical documents to {CANONICAL_DOCUMENTS}")


if __name__ == "__main__":
    main()
