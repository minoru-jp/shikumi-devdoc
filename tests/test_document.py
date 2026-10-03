import pytest

from shikumi_devdoc.norms._document import document
from shikumi_devdoc.realizers.document_markdown import MarkdownRealizer
from tests.fixtures import (
    document_merge_string,
    document_multiple_terms,
    document_reference_mismatch,
    document_repeated_term,
    document_source,
    plain_document_source,
)

CONTEXT = {
    "PROJECT": {"name": "Example", "version": "0.1.0"},
    "PYTHON": {"minimum": "3.11"},
}


def test_heading_fragment_contract_follows_rendered_heading_text() -> None:
    from shikumi_devdoc.realizers._markdown_heading import heading_fragment

    assert heading_fragment("DOC_010") == "doc_010"
    assert heading_fragment("Natural target title") == "natural-target-title"
    assert heading_fragment("設定 / 出力") == "設定-出力"
    assert heading_fragment("CLI: --output_name") == "cli---output_name"


def test_canonical_document_requires_explicit_heading_policy() -> None:
    from shikumi_devdoc.norms.common import canonical_source

    with pytest.raises(TypeError, match="requires heading"):
        canonical_source("Example", filename="example.md")
    with pytest.raises(ValueError, match="canonical heading"):
        canonical_source("Example", filename="example.md", heading="automatic")


def test_title_writer_is_assignment_only_and_supports_local_merge() -> None:
    from shikumi_devdoc.norms.document import title
    from tests.fixtures import document_title_merge

    assert not callable(title)

    result = document.validate(document_title_merge, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer(CONTEXT).realize(result.view)
    by_name = {item.filename: item.content for item in rendered}

    assert "## Widget for Example" in by_name["title-heading.md"]
    assert "title:" not in by_name["title-heading.md"]
    assert "## SPEC_001" in by_name["identity-heading.md"]
    assert "title: Widget for Example" in by_name["identity-heading.md"]


def test_nested_reference_targets_require_identity_heading_policy() -> None:
    from tests.fixtures import document_reference_title_target

    result = document.validate(document_reference_title_target, placement=())
    assert not result.is_valid
    assert "document.reference.target.heading" in {
        diagnostic.code for diagnostic in result.diagnostics
    }


def test_title_heading_document_root_remains_referenceable() -> None:
    from tests.fixtures import document_reference_title_root

    result = document.validate(document_reference_title_root, placement=())
    assert result.is_valid, result.diagnostics
    rendered = {
        item.filename: item.content for item in MarkdownRealizer().realize(result.view)
    }
    assert "related: [Narrative target](target-root.md)" in rendered["source-root.md"]


def test_document_docstrings_are_cleandoc_normalized_before_semantic_view() -> None:
    from shikumi_devdoc.norms._common import CanonicalContent
    from tests.fixtures import document_indented_docstrings

    result = document.validate(document_indented_docstrings, placement=())
    assert result.is_valid, result.diagnostics

    by_subject = {item.subject: item for item in result.view.entities}
    assert by_subject[document_indented_docstrings.ROOT].values(CanonicalContent) == (
        "Root content.\n\n    Root relative indentation.",
    )
    assert by_subject[document_indented_docstrings.ROOT.CHILD].values(
        CanonicalContent
    ) == ("Child content.\n\n    Child relative indentation.",)


def test_document_with_vocabulary_and_context_renders_markdown() -> None:
    result = document.validate(document_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = MarkdownRealizer(
        CONTEXT,
        header_comment=(
            "生成物です。\n"
            "正本は `tests/fixtures/document_source.py` です。\n\n"
            "公開時はこのコメントを除外する。"
        ),
    )
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)[0]
    assert rendered.content == (
        "<!--\n"
        "生成物です。\n"
        "正本は `tests/fixtures/document_source.py` です。\n\n"
        "公開時はこのコメントを除外する。\n"
        "-->\n\n"
        "# Example\n\n"
        "Version 0.1.0 documents the Widget API.\n\n"
        "Translation-sensitive identifier: InternalName.\n\n"
        "## Install\n\n"
        "Requires Python 3.11+.\n"
    )


def test_document_vocabulary_is_optional() -> None:
    result = document.validate(plain_document_source, placement=())
    assert result.is_valid, result.diagnostics

    rendered = MarkdownRealizer({"PROJECT": {"name": "Plain"}}).realize(result.view)[0]
    assert rendered.filename == "plain_document_source.md"
    assert rendered.content.startswith("# Plain\n")


def test_string_merge_is_local_literal_and_precedes_external_context() -> None:
    result = document.validate(document_merge_string, placement=())
    assert result.is_valid, result.diagnostics

    realizer = MarkdownRealizer({"value": "external", "external": "expanded"})
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)[0]
    assert rendered.content == "# Merge\n\nLocal {{external}}\n"


def test_missing_placeholder_fails_check() -> None:
    view = document.view(document_source, placement=())
    check = MarkdownRealizer({"PROJECT": {"name": "Example"}}).check(view)

    assert not check.is_realizable
    codes = {diagnostic.code for diagnostic in check.diagnostics}
    assert "markdown.document.placeholder.unknown" in codes


def test_header_comment_is_supplied_by_caller() -> None:
    view = document.view(plain_document_source, placement=())
    rendered = MarkdownRealizer(
        {"PROJECT": {"name": "Plain"}},
        header_comment="運用側の注意書き\n\n運用側の公開方針",
    ).realize(view)[0]
    assert rendered.content.startswith(
        "<!--\n運用側の注意書き\n\n運用側の公開方針\n-->\n\n# Plain\n"
    )


def test_merge_bindings_are_local_to_each_document_node() -> None:
    result = document.validate(document_reference_mismatch, placement=())
    assert result.is_valid, result.diagnostics

    check = MarkdownRealizer().check(result.view)
    assert not check.is_realizable
    diagnostics = {
        (diagnostic.code, diagnostic.subject) for diagnostic in check.diagnostics
    }
    assert (
        "markdown.document.placeholder.forbidden",
        document_reference_mismatch.TITLE_1.TITLE_2,
    ) in diagnostics


def test_repeated_term_marker_needs_only_one_reference() -> None:
    result = document.validate(document_repeated_term, placement=())
    assert result.is_valid, result.diagnostics


def test_multiple_vocabulary_terms_expand_in_one_document_body() -> None:
    result = document.validate(document_multiple_terms, placement=())
    assert result.is_valid, result.diagnostics

    realizer = MarkdownRealizer()
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    rendered = realizer.realize(result.view)[0]

    assert "Widget uses InternalName." in rendered.content


def test_markdown_check_warns_about_raw_headings_and_rejects_depth_over_six() -> None:
    from tests.fixtures import document_structural_markdown

    result = document.validate(document_structural_markdown, placement=())
    assert result.is_valid, result.diagnostics

    check = MarkdownRealizer().check(result.view)
    diagnostics = {diagnostic.code: diagnostic for diagnostic in check.diagnostics}

    assert "markdown.document.heading.raw" in diagnostics
    assert diagnostics["markdown.document.heading.raw"].severity.value == "warning"
    assert "body line 7" in diagnostics["markdown.document.heading.raw"].message
    assert "markdown.document.heading.depth" in diagnostics
    assert not check.is_realizable


def test_related_field_can_remain_source_only_under_ignore_policy() -> None:
    from shikumi_devdoc.norms._document import DocumentField, FieldValue
    from tests.fixtures import document_related
    from tests.fixtures.document_related_targets import API_TARGET, SPEC_TARGET

    result = document.validate(document_related, placement=())
    assert result.is_valid, result.diagnostics

    root = next(
        item
        for item in result.view.entities
        if item.subject is document_related.TITLE_1
    )
    related_values = [
        entry.value
        for entry in root.values(DocumentField)
        if isinstance(entry, FieldValue) and entry.schema.name == "related"
    ]
    assert related_values == [(SPEC_TARGET, API_TARGET)]

    rendered = MarkdownRealizer().realize(result.view)[0]
    assert rendered.content == (
        "# Guide\n\n"
        "Purpose-oriented explanation whose source records structured relations.\n\n"
        "## Usage\n\n"
        "The rendered prose remains independent of relation presentation.\n"
    )
    assert "Related" not in rendered.content
    assert "RELATED-SPEC_001" not in rendered.content
    assert "example.Widget" not in rendered.content


def test_related_field_uses_normal_append_policy() -> None:
    from tests.fixtures import document_related_append

    result = document.validate(document_related_append, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer().realize(result.view)[0]
    assert (
        "related: [SPEC_TARGET](targets.md#spec_target), "
        "[API_TARGET](targets.md#api_target)"
    ) in rendered.content

    from tests.fixtures import document_related_targets

    target_result = document.validate(document_related_targets, placement=())
    assert target_result.is_valid, target_result.diagnostics
    target_rendered = MarkdownRealizer().realize(target_result.view)[0]
    assert "## SPEC_TARGET" in target_rendered.content
    assert "## API_TARGET" in target_rendered.content
    assert "<a id=" not in target_rendered.content


def test_document_related_accepts_any_resolved_python_class_target() -> None:
    from shikumi_devdoc.norms._document import DocumentField, FieldValue
    from tests.fixtures import document_related_plain
    from tests.fixtures.related_plain_target import PLAIN_TARGET

    result = document.validate(document_related_plain, placement=())
    assert result.is_valid, result.diagnostics
    root = next(
        item
        for item in result.view.entities
        if item.subject is document_related_plain.TITLE_1
    )
    related_values = [
        entry.value
        for entry in root.values(DocumentField)
        if isinstance(entry, FieldValue) and entry.schema.name == "related"
    ]
    assert related_values == [(PLAIN_TARGET,)]
    rendered = MarkdownRealizer().realize(result.view)[0]
    assert "related: `PLAIN_TARGET`" in rendered.content


def test_implicit_merge_uses_shortest_unique_python_name() -> None:
    from tests.fixtures import document_implicit_term

    result = document.validate(document_implicit_term, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer().realize(result.view)[0]
    assert "Alpha." in rendered.content


def test_implicit_merge_can_disambiguate_with_vocabulary_class_name() -> None:
    from tests.fixtures import document_qualified_terms

    result = document.validate(document_qualified_terms, placement=())
    assert result.is_valid, result.diagnostics
    realizer = MarkdownRealizer()
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    rendered = realizer.realize(result.view)[0]
    assert "Alpha and Beta." in rendered.content


def test_implicit_merge_reports_only_an_ambiguous_reference() -> None:
    from tests.fixtures import document_ambiguous_term

    result = document.validate(document_ambiguous_term, placement=())
    assert not result.is_valid
    diagnostics = [
        diagnostic
        for diagnostic in result.diagnostics
        if diagnostic.code == "document.reference.ambiguous"
    ]
    assert len(diagnostics) == 1
    assert "VocabularyA.TERM_001" in diagnostics[0].message
    assert "VocabularyB.TERM_001" in diagnostics[0].message

    view = document.view(document_ambiguous_term, placement=())
    check = MarkdownRealizer().check(view)
    assert "markdown.document.reference.ambiguous" in {
        diagnostic.code for diagnostic in check.diagnostics
    }


def test_implicit_merge_can_extend_to_module_identity_when_container_names_collide() -> (
    None
):
    from tests.fixtures import document_module_qualified_terms

    result = document.validate(document_module_qualified_terms, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer().realize(result.view)[0]
    assert "Gamma and Delta." in rendered.content


def test_explicit_reference_collision_is_allowed_until_used() -> None:
    from tests.fixtures import document_unused_reference_collision

    result = document.validate(document_unused_reference_collision, placement=())
    assert result.is_valid, result.diagnostics
    check = MarkdownRealizer().check(result.view)
    assert check.is_realizable, check.diagnostics


def test_explicit_reference_collision_fails_when_ambiguous_name_is_used() -> None:
    from tests.fixtures import document_used_reference_collision

    result = document.validate(document_used_reference_collision, placement=())
    assert not result.is_valid
    assert "document.reference.ambiguous" in {
        diagnostic.code for diagnostic in result.diagnostics
    }


def test_reference_field_renders_same_document_heading_fragment_link() -> None:
    from tests.fixtures import document_reference_same

    result = document.validate(document_reference_same, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer().realize(result.view)[0]

    assert "See [SECTION_001](#section_001) for the stable target." in rendered.content
    assert "## SECTION_001" in rendered.content
    assert "title: Natural target title" in rendered.content
    assert "<a id=" not in rendered.content
    assert "related:" not in rendered.content


def test_reference_field_uses_target_heading_fragment_without_requiring_joint_realization() -> (
    None
):
    from tests.fixtures import (
        document_reference_nested_source,
        document_reference_nested_target,
    )

    source_result = document.validate(document_reference_nested_source, placement=())
    assert source_result.is_valid, source_result.diagnostics
    source_rendered = MarkdownRealizer().realize(source_result.view)[0]
    assert "related: [SPEC_050](runtime-targets.md#spec_050)" in source_rendered.content
    assert "SECTION_502.SPEC_050`" not in source_rendered.content

    target_result = document.validate(document_reference_nested_target, placement=())
    assert target_result.is_valid, target_result.diagnostics
    target_rendered = MarkdownRealizer().realize(target_result.view)[0]
    assert "## SECTION_502" in target_rendered.content
    assert "title: Runtime target resolution" in target_rendered.content
    assert "### SPEC_050" in target_rendered.content
    assert "<a id=" not in target_rendered.content


def test_reference_field_uses_relative_logical_document_path() -> None:
    from tests.fixtures.logical_reference_source import document as source

    result = document.validate(source, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer().realize(result.view)[0]

    assert (
        "related: [SPEC_001](../logical_reference_target/target.md#spec_001)"
        in rendered.content
    )


def test_reference_field_distinguishes_document_identity_from_filename_equality() -> (
    None
):
    from tests.fixtures import document_reference_same_filename_source

    result = document.validate(document_reference_same_filename_source, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer().realize(result.view)[0]

    # Distinct canonical roots may declare the same basename in different logical
    # collections. Filename equality alone must not turn the relation into a
    # same-document fragment reference.
    assert "related: [SPEC_001](collision.md#spec_001)" in rendered.content
