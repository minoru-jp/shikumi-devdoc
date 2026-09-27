from tests.fixtures import document_literal_placeholders
from shikumi_devdoc.norms.document import document
from shikumi_devdoc.realizers.document_markdown import MarkdownRealizer
from shikumi_devdoc.realizers._placeholders import PlaceholderResolver


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

    rendered = realizer.realize(result.view)
    assert "`${{ matrix.os }}`" in rendered
    assert "`{{TERM_1}}`" in rendered
    assert "InternalName" in rendered
