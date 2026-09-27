"""Translation-source wrapper preserving semantic vocabulary policy in Markdown."""

from __future__ import annotations

from dataclasses import dataclass, replace
import json
from types import ModuleType

from shikumi import Diagnostic, RealizationCheck, Realizer, SemanticView, information_of

from shikumi_devdoc.norms._common import MergeBinding
from shikumi_devdoc.norms._vocabulary import (
    PreserveSpelling,
    TermName,
    canonical_vocabulary_term,
)
from .markdown_document import MarkdownDocument


@dataclass(frozen=True, slots=True)
class PreserveSpellingTerm:
    """One vocabulary term whose surface spelling must survive translation."""

    source: str
    identifier: str
    text: str


@dataclass(frozen=True, slots=True)
class TranslationManifest:
    """Semantic information that must cross the Markdown translation boundary."""

    preserve_spelling: tuple[PreserveSpellingTerm, ...] = ()

    def to_json(self) -> str:
        """Render a stable, human-readable JSON representation."""

        payload = {
            "version": 1,
            "publication": "omit-this-comment",
            "preserve_spelling": [
                {
                    "source": term.source,
                    "identifier": term.identifier,
                    "text": term.text,
                }
                for term in self.preserve_spelling
            ],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)


MarkdownRealization = str | MarkdownDocument | tuple[MarkdownDocument, ...]


class TranslationSourceRealizer(Realizer[MarkdownRealization]):
    """Wrap a Markdown realizer and embed translation-relevant semantics."""

    def __init__(self, markdown_realizer: Realizer) -> None:
        self.markdown_realizer = markdown_realizer

    def check(self, view: SemanticView) -> RealizationCheck:
        base = self.markdown_realizer.check(view)
        _, diagnostics = translation_manifest(view)
        return RealizationCheck(view, (*base.diagnostics, *diagnostics))

    def realize(self, view: SemanticView) -> MarkdownRealization:
        rendered = self.markdown_realizer.realize(view)
        manifest, _ = translation_manifest(view)
        if not manifest.preserve_spelling:
            return rendered

        def add_metadata(content: str) -> str:
            return (
                "<!-- shikumi-devdoc:translation-metadata\n"
                f"{manifest.to_json()}\n"
                "-->\n\n"
                f"{content}"
            )

        if isinstance(rendered, str):
            return add_metadata(rendered)
        if isinstance(rendered, MarkdownDocument):
            return replace(rendered, content=add_metadata(rendered.content))
        return tuple(
            replace(document, content=add_metadata(document.content))
            for document in rendered
        )


def _information_values(subject: object, information_type) -> tuple[object, ...]:
    return tuple(
        record.value
        for record in information_of(subject)
        if record.type is information_type
    )


def _term_manifest_entry(target: object) -> PreserveSpellingTerm | None:
    canonical = canonical_vocabulary_term(target)
    if canonical is None:
        return None
    if _information_values(canonical, PreserveSpelling) != (True,):
        return None
    names = _information_values(canonical, TermName)
    if len(names) != 1 or not isinstance(names[0], str):
        return None
    return PreserveSpellingTerm(
        source=getattr(canonical, "__module__", "<vocabulary>"),
        identifier=getattr(canonical, "__name__", "<term>"),
        text=names[0],
    )


def translation_manifest(view: SemanticView) -> tuple[TranslationManifest, tuple[Diagnostic, ...]]:
    """Collect translation policy from direct Vocabulary views or merge targets.

    A canonical document no longer attaches an entire Vocabulary. Translation
    policy follows the Vocabulary term objects that are explicitly bound through
    ``merge``. A direct Vocabulary view still exposes every preserve-spelling
    term because the Vocabulary itself is the realization subject.
    """

    diagnostics: list[Diagnostic] = []
    preserved: list[PreserveSpellingTerm] = []

    if any(item.has(TermName) for item in view.entities):
        source_name = _view_source_name(view)
        for item in view.entities:
            if item.values(PreserveSpelling) != (True,):
                continue
            names = item.values(TermName)
            if len(names) != 1:
                diagnostics.append(
                    Diagnostic(
                        "translation metadata requires exactly one term name",
                        code="translation.term.name.required",
                        subject=item.subject,
                    )
                )
                continue
            preserved.append(
                PreserveSpellingTerm(
                    source=source_name,
                    identifier=item.node.name,
                    text=names[0],
                )
            )
    else:
        seen: set[type[object]] = set()
        for item in view.entities:
            for binding in item.values(MergeBinding):
                if not isinstance(binding, tuple) or len(binding) != 2:
                    continue
                target = binding[1]
                canonical = canonical_vocabulary_term(target)
                if canonical is None or canonical in seen:
                    continue
                seen.add(canonical)
                entry = _term_manifest_entry(canonical)
                if entry is not None:
                    preserved.append(entry)

    preserved.sort(key=lambda term: (term.source, term.identifier, term.text))
    return TranslationManifest(tuple(preserved)), tuple(diagnostics)


def _view_source_name(view: SemanticView) -> str:
    subject = view.focused.subject
    if isinstance(subject, ModuleType):
        return getattr(subject, "__name__", "<vocabulary>")
    return getattr(subject, "__module__", "<vocabulary>")
