import shikumi_devdoc
from shikumi_devdoc import Context, fields, norms, realizers
from shikumi_devdoc.fields import (
    api_reference as api_reference_fields,
    changelog as changelog_fields,
    common as common_fields,
    lifecycle as lifecycle_fields,
    specification as specification_fields,
    status as status_fields,
)
from shikumi_devdoc.norms import common, document, vocabulary
from shikumi_devdoc.realizers import (
    common as common_realizers,
    document as document_realizers,
    index as index_realizers,
    translation as translation_realizers,
    vocabulary as vocabulary_realizers,
)


def test_top_level_public_api_is_small_and_namespaced() -> None:
    assert Context is shikumi_devdoc.Context
    assert fields is shikumi_devdoc.fields
    assert norms is shikumi_devdoc.norms
    assert realizers is shikumi_devdoc.realizers

    for old_flat_name in (
        "canonical",
        "canonical_source",
        "spec",
        "MUST",
        "SpecificationMarkdownRealizer",
    ):
        assert not hasattr(shikumi_devdoc, old_flat_name)




def test_standard_fields_public_api_is_namespaced_and_generic() -> None:
    assert set(fields.__all__) == {
        "api_reference",
        "changelog",
        "common",
        "lifecycle",
        "specification",
        "status",
    }

    assert set(common_fields.__all__) == {"condition", "detail", "kind", "related"}
    assert not hasattr(common_fields, "title")
    assert not hasattr(specification_fields, "title")
    assert specification_fields.condition is common_fields.condition
    assert specification_fields.related is common_fields.related
    assert specification_fields.MUST == "MUST"
    assert specification_fields.MAY == "MAY"

    assert api_reference_fields.kind is common_fields.kind
    assert api_reference_fields.detail is common_fields.detail
    assert api_reference_fields.related is common_fields.related
    assert api_reference_fields.OPERATION == "Operation"

    assert not hasattr(status_fields, "title")
    assert status_fields.kind is common_fields.kind
    assert status_fields.GENERAL == "General"

    assert changelog_fields.version is not None
    assert changelog_fields.added is not None

    assert set(lifecycle_fields.__all__) == {
        "deprecated",
        "introduced",
        "migration",
        "removed",
        "replacement",
    }
    assert lifecycle_fields.introduced.name == "introduced"
    assert lifecycle_fields.deprecated.name == "deprecated"
    assert lifecycle_fields.removed.name == "removed"
    assert lifecycle_fields.replacement.name == "replacement"
    assert lifecycle_fields.migration.name == "migration"


def test_norms_public_api_is_grouped_by_domain() -> None:
    assert set(norms.__all__) == {"common", "document", "vocabulary"}

    assert common.canonical_source is not None
    assert common.summary is not None
    assert common.APPEND is not None
    assert common.IGNORE is not None
    assert common.merge is not None
    assert not hasattr(common, "related")

    assert set(document.__all__) == {
        "test_target_field",
        "field",
        "list_field",
        "prose_field",
        "reference_field",
        "system",
        "table_field",
        "title",
    }
    assert document.field is not None
    assert document.list_field is not None
    assert document.test_target_field is not None
    assert document.test_target_field.__test__ is False
    assert not hasattr(document, "code_field")
    assert document.table_field is not None
    assert document.prose_field is not None
    assert document.title is not None
    assert not callable(document.title)
    assert document.system is not None

    assert set(vocabulary.__all__) == {
        "alias",
        "deprecated",
        "glossary",
        "preserve_spelling",
        "replacement",
        "system",
        "vocabulary",
    }
    assert vocabulary.vocabulary is not None
    assert vocabulary.system is not None
    assert not hasattr(vocabulary, "term")
    assert not hasattr(vocabulary, "title")

    assert not hasattr(norms, "itemized")
    assert not hasattr(norms, "specification")
    assert not hasattr(norms, "api_reference")


def test_domain_keywords_are_not_part_of_generic_document_core() -> None:
    for name in ("MUST", "OPERATION", "requirement", "input", "output"):
        assert not hasattr(document, name)


def test_realizers_public_api_is_grouped_by_domain() -> None:
    assert set(realizers.__all__) == {
        "common",
        "document",
        "index",
        "translation",
        "vocabulary",
    }
    assert common_realizers.MarkdownDocument is not None
    assert document_realizers.MarkdownRealizer is not None
    assert index_realizers.IndexMarkdownRealizer is not None
    assert vocabulary_realizers.GlossaryMarkdownRealizer is not None
    assert translation_realizers.SourceRealizer is not None

    assert not hasattr(realizers, "itemized")
    assert not hasattr(realizers, "specification")
    assert not hasattr(realizers, "api_reference")


def test_every_public_namespace_exports_every_declared_name() -> None:
    namespaces = [
        fields,
        common_fields,
        specification_fields,
        api_reference_fields,
        changelog_fields,
        status_fields,
        norms,
        common,
        document,
        vocabulary,
        realizers,
        common_realizers,
        document_realizers,
        index_realizers,
        vocabulary_realizers,
        translation_realizers,
    ]
    for namespace in namespaces:
        for name in namespace.__all__:
            assert getattr(namespace, name) is not None


def test_old_document_grammar_exports_are_not_public() -> None:
    for name in ("canonical", "narrative", "itemized"):
        assert not hasattr(common, name)
        assert not hasattr(document, name)
