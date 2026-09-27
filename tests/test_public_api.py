from shikumi_devdoc import (
    Context,
    canonical,
    vocabulary,
    vocabulary_refs,
)
from shikumi_devdoc.norms import CanonicalSource, VocabularyReference, VocabularySource
from shikumi_devdoc.realizers import ChangelogMarkdownRealizer, DocumentMarkdownRealizer, GlossaryMarkdownRealizer, PythonReferenceModuleRealizer


def test_public_api_imports() -> None:
    assert Context is not None
    assert canonical is not None
    assert vocabulary is not None
    assert vocabulary_refs is not None
    assert CanonicalSource is not None
    assert VocabularySource is not None
    assert VocabularyReference is not None
    assert DocumentMarkdownRealizer is not None
    assert GlossaryMarkdownRealizer is not None
    assert ChangelogMarkdownRealizer is not None
    assert PythonReferenceModuleRealizer is not None
