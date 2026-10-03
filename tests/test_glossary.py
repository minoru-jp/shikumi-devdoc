from shikumi_devdoc.norms._vocabulary import (
    Definition,
    Glossary,
    PreserveSpelling,
    TermName,
    vocabulary_system,
)
from shikumi_devdoc.realizers.glossary_markdown import MarkdownRealizer
from tests.fixtures import vocabulary_source


def test_glossary_renders_only_public_entries_and_context() -> None:
    result = vocabulary_system.validate(vocabulary_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = MarkdownRealizer(
        {"PROJECT": {"name": "Example"}},
        header_comment="運用側の注意書き\n\n運用側の公開方針",
    )
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    public = next(item for item in result.view.entities if item.node.name == "TERM_1")
    private = next(item for item in result.view.entities if item.node.name == "TERM_2")
    assert public.values(Glossary) == ()
    assert private.values(Glossary) == (False,)

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
    from shikumi_devdoc.norms._vocabulary import Alias, Deprecated, Replacement
    from tests.fixtures import vocabulary_lifecycle

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


def test_vocabulary_accepts_indented_docstring_term_declaration() -> None:
    from tests.fixtures import vocabulary_indented_declaration

    result = vocabulary_system.validate(vocabulary_indented_declaration, placement=())
    assert result.is_valid, result.diagnostics

    term = next(item for item in result.view.entities if item.node.name == "Widget")
    assert term.values(TermName) == ("Widget",)
    assert term.values(Definition) == (
        "A named vocabulary entry.\n\n    Relative indentation remains part of the definition.",
    )


def test_vocabulary_requires_declaration_at_normalized_docstring_start() -> None:
    from tests.fixtures import vocabulary_invalid_declaration

    result = vocabulary_system.validate(vocabulary_invalid_declaration, placement=())
    assert not result.is_valid
    assert "vocabulary.term.declaration" in {d.code for d in result.diagnostics}


def test_vocabulary_allows_only_one_declaration_at_normalized_start() -> None:
    from tests.fixtures import vocabulary_multiple_declarations

    result = vocabulary_system.validate(vocabulary_multiple_declarations, placement=())
    assert not result.is_valid
    assert "vocabulary.term.declaration" in {d.code for d in result.diagnostics}


def test_vocabulary_entry_names_are_not_restricted_to_term_numbers() -> None:
    from tests.fixtures import vocabulary_named_entries

    result = vocabulary_system.validate(vocabulary_named_entries, placement=())
    assert result.is_valid, result.diagnostics
    entry = next(item for item in result.view.entities if item.node.name == "Widget")
    assert entry.values(Glossary) == (True,)
    rendered = MarkdownRealizer().realize(result.view)
    assert "## Widget" in rendered


def test_dogfood_vocabulary_produces_glossary() -> None:
    from devdocs.canonical_sources.vocabulary import canonical

    result = vocabulary_system.validate(canonical, placement=())
    assert result.is_valid, result.diagnostics

    realizer = MarkdownRealizer()
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)
    assert "## canonical source" in rendered
    assert "## canonical document" in rendered
    assert "## realization context" in rendered
    assert "## document node" in rendered
    assert "## field vocabulary" in rendered
    assert "## local reference" in rendered
    assert "## Vocabulary term" in rendered
    assert "## 表記維持" in rendered
