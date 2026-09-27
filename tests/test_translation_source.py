import json

from shikumi import RealizationCheck, Realizer, SemanticView

from tests.fixtures import document_source, structured_document_source, vocabulary_source
from shikumi_devdoc.norms._document import document
from shikumi_devdoc.norms.document import system as document_system
from shikumi_devdoc.norms._vocabulary import vocabulary_system
from shikumi_devdoc.realizers.common import MarkdownDocument
from shikumi_devdoc.realizers.document import MarkdownRealizer as DocumentMarkdownRealizer
from shikumi_devdoc.realizers.translation import (
    SourceRealizer as TranslationSourceRealizer,
    translation_manifest,
)
from shikumi_devdoc.realizers.vocabulary import GlossaryMarkdownRealizer


CONTEXT = {
    "PROJECT": {"name": "Example", "version": "0.1.0"},
    "PYTHON": {"minimum": "3.11"},
}


def test_translation_manifest_carries_preserve_spelling_from_merged_vocabulary_term() -> None:
    result = document.validate(document_source, placement=())
    manifest, diagnostics = translation_manifest(result.view)

    assert diagnostics == ()
    assert [(term.identifier, term.text) for term in manifest.preserve_spelling] == [
        ("TERM_2", "InternalName")
    ]


def test_translation_source_realizer_embeds_machine_readable_metadata() -> None:
    result = document.validate(document_source, placement=())
    realizer = TranslationSourceRealizer(DocumentMarkdownRealizer(CONTEXT))

    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)
    assert isinstance(rendered, tuple)
    assert len(rendered) == 1
    realized_document = rendered[0]
    assert isinstance(realized_document, MarkdownDocument)
    assert realized_document.filename == "document_source.md"
    prefix, markdown = realized_document.content.split("-->\n\n", 1)
    payload = prefix.split("\n", 1)[1]
    metadata = json.loads(payload)

    assert metadata["publication"] == "omit-this-comment"
    assert metadata["preserve_spelling"] == [
        {
            "source": "tests.fixtures.vocabulary_source",
            "identifier": "TERM_2",
            "text": "InternalName",
        }
    ]
    assert markdown.startswith("# Example\n")


def test_translation_manifest_can_be_built_directly_from_vocabulary_view() -> None:
    result = vocabulary_system.validate(vocabulary_source, placement=())
    realizer = TranslationSourceRealizer(GlossaryMarkdownRealizer(CONTEXT))

    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    assert '"text": "InternalName"' in realizer.realize(result.view)


class _MultiDocumentRealizer(Realizer[tuple[MarkdownDocument, ...]]):
    def check(self, view: SemanticView) -> RealizationCheck:
        return RealizationCheck(view, ())

    def realize(self, view: SemanticView) -> tuple[MarkdownDocument, ...]:
        return (
            MarkdownDocument("one.md", "# One\n"),
            MarkdownDocument("two.md", "# Two\n"),
        )


def test_translation_source_realizer_preserves_multi_document_shape() -> None:
    result = document.validate(document_source, placement=())
    realizer = TranslationSourceRealizer(_MultiDocumentRealizer())

    rendered = realizer.realize(result.view)
    assert isinstance(rendered, tuple)
    assert [document.filename for document in rendered] == ["one.md", "two.md"]
    assert all(
        document.content.startswith("<!-- shikumi-devdoc:translation-metadata\n")
        for document in rendered
    )


def test_translation_source_realizer_adds_no_metadata_without_vocabulary_policy() -> None:
    result = document_system.validate(structured_document_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = TranslationSourceRealizer(DocumentMarkdownRealizer({"PROJECT": {"name": "Demo"}}))
    rendered = realizer.realize(result.view)

    assert isinstance(rendered, tuple)
    assert len(rendered) == 2
    assert all(
        not document.content.startswith("<!-- shikumi-devdoc:translation-metadata")
        for document in rendered
    )
