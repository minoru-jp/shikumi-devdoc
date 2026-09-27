import json

from tests.fixtures import document_source, vocabulary_source
from shikumi_devdoc.norms.document import document
from shikumi_devdoc.norms.vocabulary import vocabulary_system
from shikumi_devdoc.realizers import (
    DocumentMarkdownRealizer,
    GlossaryMarkdownRealizer,
    TranslationSourceRealizer,
    translation_manifest,
)


CONTEXT = {
    "PROJECT": {"name": "Example", "version": "0.1.0"},
    "PYTHON": {"minimum": "3.11"},
}


def test_translation_manifest_carries_preserve_spelling_from_attached_vocabulary() -> None:
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
    prefix, markdown = rendered.split("-->\n\n", 1)
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
