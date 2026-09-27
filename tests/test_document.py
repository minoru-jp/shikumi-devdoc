from tests.fixtures import (
    document_reference_mismatch,
    document_repeated_term,
    document_source,
    plain_document_source,
)
from shikumi_devdoc.norms.document import document
from shikumi_devdoc.realizers.document_markdown import MarkdownRealizer


CONTEXT = {
    "PROJECT": {"name": "Example", "version": "0.1.0"},
    "PYTHON": {"minimum": "3.11"},
}


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

    rendered = realizer.realize(result.view)
    assert rendered == (
        "<!--\n"
        "生成物です。\n"
        "正本は `tests/fixtures/document_source.py` です。\n\n"
        "公開時はこのコメントを除外する。\n"
        "-->\n\n"
        "# Example\n\n"
        "Version 0.1.0 documents the Widget API.\n\n"
        "## Install\n\n"
        "Requires Python 3.11+.\n"
    )


def test_document_vocabulary_is_optional() -> None:
    result = document.validate(plain_document_source, placement=())
    assert result.is_valid, result.diagnostics

    rendered = MarkdownRealizer({"PROJECT": {"name": "Plain"}}).realize(result.view)
    assert rendered.startswith("# Plain\n")


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
    ).realize(view)
    assert rendered.startswith(
        "<!--\n運用側の注意書き\n\n運用側の公開方針\n-->\n\n# Plain\n"
    )


def test_vocabulary_references_are_validated_per_entity() -> None:
    result = document.validate(document_reference_mismatch, placement=())
    assert not result.is_valid

    diagnostics = {(diagnostic.code, diagnostic.subject) for diagnostic in result.diagnostics}
    assert (
        "document.vocabulary_reference.unused",
        document_reference_mismatch.TITLE_1,
    ) in diagnostics
    assert (
        "document.vocabulary_reference.missing",
        document_reference_mismatch.TITLE_1.TITLE_2,
    ) in diagnostics


def test_repeated_term_marker_needs_only_one_reference() -> None:
    result = document.validate(document_repeated_term, placement=())
    assert result.is_valid, result.diagnostics


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


def test_stable_anchors_and_section_references_render_without_duplicate_declarations() -> None:
    from tests.fixtures import document_anchor_source

    result = document.validate(document_anchor_source, placement=())
    assert result.is_valid, result.diagnostics

    from shikumi_devdoc.norms.document import SectionReference

    root = next(
        item for item in result.view.entities
        if item.subject is document_anchor_source.TITLE_1
    )
    assert root.values(SectionReference) == ("install",)

    realizer = MarkdownRealizer()
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)
    assert rendered == (
        '<a id="guide"></a>\n\n'
        '# Guide\n\n'
        'Start with [Install \\[Linux\\]](#install). Write `{{#literal}}` to show the marker literally.\n\n'
        '<a id="install"></a>\n\n'
        '## Install [Linux]\n\n'
        'Installation instructions.\n'
    )


def test_unknown_section_reference_fails_semantic_validation() -> None:
    from tests.fixtures import document_anchor_unknown

    result = document.validate(document_anchor_unknown, placement=())
    diagnostics = {diagnostic.code for diagnostic in result.diagnostics}

    assert "document.section_reference.unknown" in diagnostics
    assert not result.is_valid


def test_document_rejects_duplicate_and_invalid_anchor_names() -> None:
    from tests.fixtures import document_anchor_invalid

    result = document.validate(document_anchor_invalid, placement=())
    codes = [diagnostic.code for diagnostic in result.diagnostics]

    assert "document.anchor.duplicate" in codes
    assert "document.anchor.syntax" in codes
    assert not result.is_valid


def test_section_reference_marker_is_not_allowed_in_heading_title() -> None:
    from tests.fixtures import document_anchor_title_invalid

    result = document.validate(document_anchor_title_invalid, placement=())
    codes = {diagnostic.code for diagnostic in result.diagnostics}

    assert "document.section_reference.title" in codes
    assert not result.is_valid
