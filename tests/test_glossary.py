from tests.fixtures import vocabulary_source
from shikumi_devdoc.norms.vocabulary import PreserveSpelling, vocabulary_system
from shikumi_devdoc.realizers.glossary_markdown import MarkdownRealizer


def test_glossary_renders_only_public_entries_and_context() -> None:
    result = vocabulary_system.validate(vocabulary_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = MarkdownRealizer(
        {"PROJECT": {"name": "Example"}},
        header_comment="運用側の注意書き\n\n運用側の公開方針",
    )
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)
    assert rendered == (
        "<!--\n"
        "運用側の注意書き\n\n"
        "運用側の公開方針\n"
        "-->\n\n"
        "# Example Glossary\n\n"
        "Terms used by Example.\n\n"
        "## Widget\n\n"
        "A reusable widget.\n"
    )
    assert "InternalName" not in rendered


def test_vocabulary_preserve_spelling_is_semantic_information() -> None:
    result = vocabulary_system.validate(vocabulary_source, placement=())
    assert result.is_valid, result.diagnostics

    term = next(item for item in result.view.entities if item.node.name == "TERM_2")
    assert term.values(PreserveSpelling) == (True,)


def test_vocabulary_alias_and_deprecation_render_as_public_semantics() -> None:
    from tests.fixtures import vocabulary_lifecycle
    from shikumi_devdoc.norms.vocabulary import Alias, Deprecated, Replacement

    result = vocabulary_system.validate(vocabulary_lifecycle, placement=())
    assert result.is_valid, result.diagnostics

    current = next(item for item in result.view.entities if item.node.name == "TERM_1")
    old = next(item for item in result.view.entities if item.node.name == "TERM_2")
    assert current.values(Alias) == ("Component", "UI Widget")
    assert old.values(Deprecated) == (True,)
    assert old.values(Replacement) == ("Widget",)

    rendered = MarkdownRealizer().realize(result.view)
    assert "**Aliases:** Component, UI Widget" in rendered
    assert "> **Deprecated.** Use Widget instead." in rendered


def test_vocabulary_relationships_reject_collisions_and_unknown_replacements() -> None:
    from tests.fixtures import vocabulary_invalid_lifecycle

    result = vocabulary_system.validate(vocabulary_invalid_lifecycle, placement=())
    assert not result.is_valid
    codes = {diagnostic.code for diagnostic in result.diagnostics}
    assert "vocabulary.alias.conflict" in codes
    assert "vocabulary.replacement.target" in codes
