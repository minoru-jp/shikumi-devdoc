from shikumi_devdoc.norms._document import document
from shikumi_devdoc.realizers._placeholders import PlaceholderResolver
from shikumi_devdoc.realizers.document_markdown import MarkdownRealizer
from tests.fixtures import document_literal_placeholders


def test_placeholder_resolver_distinguishes_semantic_and_literal_forms() -> None:
    resolver = PlaceholderResolver({"PROJECT": {"name": "Example"}})
    source = r"semantic={{PROJECT.name}} escaped=\{{MISSING}} host=${{ matrix.os }}"

    assert resolver.unknown(source) == ()
    assert resolver.expand(source) == (
        "semantic=Example escaped={{MISSING}} host=${{ matrix.os }}"
    )


def test_literal_term_marker_is_not_a_vocabulary_reference() -> None:
    result = document.validate(document_literal_placeholders, placement=())
    assert result.is_valid, result.diagnostics

    realizer = MarkdownRealizer()
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)[0]
    assert "`${{ matrix.os }}`" in rendered.content
    assert "`{{widget}}`" in rendered.content
    assert "InternalName" in rendered.content


def test_canonical_document_can_forbid_external_placeholders() -> None:
    from shikumi_devdoc.norms.document import system
    from tests.fixtures import root_placeholders_forbidden

    result = system.validate(root_placeholders_forbidden, placement=())
    assert result.is_valid, result.diagnostics
    check = MarkdownRealizer({"PROJECT": {"version": "1.0"}}).check(result.view)
    assert not check.is_realizable
    assert "markdown.document.placeholder.forbidden" in {
        d.code for d in check.diagnostics
    }


def test_placeholder_policy_is_independent_from_document_shape() -> None:
    from shikumi_devdoc.norms.document import system
    from tests.fixtures import nested_placeholders_forbidden

    result = system.validate(nested_placeholders_forbidden, placement=())
    assert result.is_valid, result.diagnostics
    check = MarkdownRealizer({"PROJECT": {"version": "1.0"}}).check(result.view)
    assert not check.is_realizable
    assert "markdown.document.placeholder.forbidden" in {
        d.code for d in check.diagnostics
    }
