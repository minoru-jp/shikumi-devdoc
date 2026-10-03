from shikumi_devdoc.norms._document import document
from shikumi_devdoc.realizers.index import IndexMarkdownRealizer
from tests.fixtures import (
    index_collision,
    index_missing_summary,
    index_source,
    index_summary_placeholder_forbidden,
)
from tests.fixtures.index_source import core


def test_index_realizer_collects_package_documents_in_declared_order() -> None:
    result = document.validate(index_source)
    assert result.is_valid, result.diagnostics

    realizer = IndexMarkdownRealizer(
        {"PROJECT": {"name": "Example"}},
        title="Example Reference",
    )
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)
    assert rendered.filename == "INDEX.md"
    assert rendered.content == (
        "# Example Reference\n\n"
        "| Document | Summary |\n"
        "| --- | --- |\n"
        "| [Example Core](core.md) | Core APIs for Example. |\n"
        "| [Guide](guide.md) | Usage guidance for the package. |\n"
    )


def test_index_realizer_requires_package_focus() -> None:
    result = document.validate(core, placement=())
    assert result.is_valid, result.diagnostics

    check = IndexMarkdownRealizer({"PROJECT": {"name": "Example"}}).check(result.view)
    assert not check.is_realizable
    assert {diagnostic.code for diagnostic in check.diagnostics} == {
        "markdown.index.package.required"
    }


def test_index_realizer_rejects_index_filename_collision() -> None:
    result = document.validate(index_collision)
    assert result.is_valid, result.diagnostics

    check = IndexMarkdownRealizer().check(result.view)
    assert not check.is_realizable
    assert "markdown.index.filename.collision" in {
        diagnostic.code for diagnostic in check.diagnostics
    }


def test_index_realizer_requires_context_for_document_title_placeholders() -> None:
    result = document.validate(index_source)
    assert result.is_valid, result.diagnostics

    check = IndexMarkdownRealizer().check(result.view)
    assert not check.is_realizable
    assert "markdown.index.placeholder.unknown" in {
        diagnostic.code for diagnostic in check.diagnostics
    }


def test_index_realizer_requires_summary_for_every_document() -> None:
    result = document.validate(index_missing_summary)
    assert result.is_valid, result.diagnostics

    check = IndexMarkdownRealizer().check(result.view)
    assert not check.is_realizable
    assert "markdown.index.summary.required" in {
        diagnostic.code for diagnostic in check.diagnostics
    }


def test_index_realizer_applies_placeholder_policy_to_summary() -> None:
    result = document.validate(index_summary_placeholder_forbidden)
    assert result.is_valid, result.diagnostics

    check = IndexMarkdownRealizer({"PROJECT": {"name": "Example"}}).check(result.view)
    assert not check.is_realizable
    assert "markdown.index.placeholder.forbidden" in {
        diagnostic.code for diagnostic in check.diagnostics
    }
