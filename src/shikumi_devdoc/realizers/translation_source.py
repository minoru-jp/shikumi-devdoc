"""Translation-source wrapper preserving semantic vocabulary policy in Markdown."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import json
from types import ModuleType

from shikumi import Diagnostic, RealizationCheck, Realizer, SemanticView

from shikumi_devdoc.norms.common import VocabularySource
from shikumi_devdoc.norms.vocabulary import PreserveSpelling, TermName, vocabulary_system


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


class TranslationSourceRealizer(Realizer[str]):
    """Wrap a Markdown realizer and embed translation-relevant semantics.

    The wrapped realizer remains responsible for document rendering. This wrapper
    only carries semantic policy that would otherwise disappear after realization.
    """

    def __init__(self, markdown_realizer: Realizer[str]) -> None:
        self.markdown_realizer = markdown_realizer

    def check(self, view: SemanticView) -> RealizationCheck:
        base = self.markdown_realizer.check(view)
        _, diagnostics = translation_manifest(view)
        return RealizationCheck(view, (*base.diagnostics, *diagnostics))

    def realize(self, view: SemanticView) -> str:
        rendered = self.markdown_realizer.realize(view)
        manifest, _ = translation_manifest(view)
        if not manifest.preserve_spelling:
            return rendered
        return f"<!-- shikumi-devdoc:translation-metadata\n{manifest.to_json()}\n-->\n\n{rendered}"


def translation_manifest(view: SemanticView) -> tuple[TranslationManifest, tuple[Diagnostic, ...]]:
    """Collect translation policy from attached or directly viewed vocabularies."""

    sources = _unique_identity(
        source
        for item in view.entities
        for source in item.values(VocabularySource)
    )

    vocabulary_views: list[tuple[str, SemanticView]] = []
    diagnostics: list[Diagnostic] = []

    if sources:
        for source in sources:
            try:
                placement = () if isinstance(source, ModuleType) and not hasattr(source, "__path__") else None
                result = vocabulary_system.validate(source, placement=placement)
            except Exception as exc:
                diagnostics.append(
                    Diagnostic(
                        f"translation vocabulary could not be interpreted: {exc}",
                        code="translation.vocabulary.invalid",
                    )
                )
                continue
            if not result.is_valid:
                diagnostics.append(
                    Diagnostic(
                        "translation vocabulary does not satisfy the vocabulary regulation",
                        code="translation.vocabulary.invalid",
                        subject=source,
                    )
                )
                continue
            vocabulary_views.append((getattr(source, "__name__", "<vocabulary>"), result.view))
    elif any(item.has(TermName) for item in view.entities):
        vocabulary_views.append((_view_source_name(view), view))

    preserved: list[PreserveSpellingTerm] = []
    for source_name, vocabulary_view in vocabulary_views:
        for item in vocabulary_view.entities:
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

    preserved.sort(key=lambda term: (term.source, term.identifier, term.text))
    return TranslationManifest(tuple(preserved)), tuple(diagnostics)


def _unique_identity(values: Iterable[ModuleType]) -> list[ModuleType]:
    result: list[ModuleType] = []
    for value in values:
        if not any(existing is value for existing in result):
            result.append(value)
    return result


def _view_source_name(view: SemanticView) -> str:
    subject = view.focused.subject
    if isinstance(subject, ModuleType):
        return getattr(subject, "__name__", "<vocabulary>")
    return getattr(subject, "__module__", "<vocabulary>")
