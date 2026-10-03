import json
import re
from pathlib import Path

from devdocs.canonical_sources import api_reference, specification
from devdocs.canonical_sources import authoring_guide as authoring_guide_source
from devdocs.canonical_sources.changelog import canonical as changelog_source
from devdocs.canonical_sources.readme import canonical as readme_source
from devdocs.canonical_sources.specification.core import (
    SPECIFICATION_PART as CORE_SPEC,
)
from devdocs.canonical_sources.status import canonical as status_source
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from devdocs.canonical_sources.workspace import canonical as workspace_source
from shikumi_devdoc.norms.document import system as document

document_system = document
from shikumi_devdoc import fields as public_fields
from shikumi_devdoc import norms as public_norms
from shikumi_devdoc import realizers as public_realizers
from shikumi_devdoc.realizers.document import (
    MarkdownRealizer as DocumentMarkdownRealizer,
)
from shikumi_devdoc.realizers.index import IndexMarkdownRealizer


def _public_paths(namespace, prefix: str) -> list[str]:
    paths: list[str] = []
    for name in namespace.__all__:
        value = getattr(namespace, name)
        path = f"{prefix}.{name}"
        paths.append(path)
        child_all = getattr(value, "__all__", None)
        child_name = getattr(value, "__name__", "")
        if (
            child_all is not None
            and isinstance(child_name, str)
            and child_name.startswith(prefix)
        ):
            paths.extend(_public_paths(value, path))
    return paths


CONTEXT = json.loads(Path("devdocs/config/context.json").read_text(encoding="utf-8"))


def test_repository_readme_dogfoods_external_context_and_document_examples() -> None:
    result = document.validate(readme_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = DocumentMarkdownRealizer(CONTEXT)
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    rendered = realizer.realize(result.view)[0]
    assert rendered.filename == "README.md"
    assert rendered.content.startswith("# shikumi-devdoc\n")
    assert "## こんな開発に" in rendered.content
    assert 'merge_policy="all"' in rendered.content
    assert 'merge_policy="local"' in rendered.content
    assert "| `forbidden` |" in rendered.content
    assert (
        "https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/authoring_guide/INDEX.md"
        in rendered.content
    )
    assert (
        "https://github.com/minoru-jp/shikumi-devdoc/blob/main/STATUS.md"
        in rendered.content
    )
    assert (
        "https://github.com/minoru-jp/shikumi-devdoc/blob/main/LICENSE"
        in rendered.content
    )


def test_repository_workspace_readme_is_canonical_document() -> None:
    result = document.validate(workspace_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = DocumentMarkdownRealizer({})
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    rendered = realizer.realize(result.view)[0]
    assert rendered.content.startswith("# devdocs/")
    assert "canonical_sources/" in rendered.content
    assert "fields/terms.py" not in rendered.content
    assert "canonical_documents/" in rendered.content
    assert "intermediate" not in rendered.content.lower()
    assert "中間文書" not in rendered.content
    assert "config/context.json" in rendered.content
    assert "shikumi_devdoc/resources/devdocs/" in rendered.content
    assert "shikumi_devdoc/resources/published_docs/" in rendered.content


def test_repository_authoring_guide_is_canonical_document_collection() -> None:
    result = document_system.validate(authoring_guide_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = DocumentMarkdownRealizer({})
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    documents = realizer.realize(result.view)
    by_name = {document.filename: document.content for document in documents}
    assert set(by_name) == {
        "overview.md",
        "readme.md",
        "getting-started.md",
        "configuration-guide.md",
        "cli-documentation.md",
        "specification.md",
        "api-reference.md",
        "changelog.md",
        "glossary.md",
        "project-status.md",
        "collections.md",
        "advanced-authoring.md",
        "llm-workflow.md",
    }
    assert by_name["overview.md"].startswith("# Authoring Guide overview")
    assert "特定の文書セットを要求しない" in by_name["overview.md"]
    assert "## Specification を作る場合" in by_name["specification.md"]
    assert "## API Reference を作る場合" in by_name["api-reference.md"]
    assert "## Glossary / Vocabulary を作る場合" in by_name["glossary.md"]
    assert "Python import が循環する場合" in by_name["specification.md"]
    assert "DOC_007" not in "\n".join(by_name.values())

    index_realizer = IndexMarkdownRealizer({}, title="shikumi-devdoc Authoring Guide")
    index_check = index_realizer.check(result.view)
    assert index_check.is_realizable, index_check.diagnostics
    index = index_realizer.realize(result.view)
    assert index.filename == "INDEX.md"
    assert "[Authoring Guide overview](overview.md)" in index.content
    assert "[Writing a README](readme.md)" in index.content
    assert "[Writing a Specification](specification.md)" in index.content
    assert "[Writing an API Reference](api-reference.md)" in index.content
    assert "[Advanced authoring decisions](advanced-authoring.md)" in index.content


def test_repository_project_status_dogfoods_generic_documents() -> None:
    result = document_system.validate(status_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = DocumentMarkdownRealizer(CONTEXT)
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    documents = realizer.realize(result.view)
    assert len(documents) == 1
    status_document = documents[0]
    assert status_document.filename == "STATUS.md"
    assert "## STATUS_001" in status_document.content
    assert "title: Development stage" in status_document.content
    assert "## NOTICE_001" in status_document.content
    assert "kind: General" in status_document.content
    assert (
        "condition: `0.3.0` の Beta 公開から最初のメジャーバージョンへ移行するまで。"
        in status_document.content
    )
    assert "Installed documentation resources" in status_document.content
    assert "shikumi>=0.2.0" in status_document.content
    assert "GitHub Actions" in status_document.content
    assert "Trusted Publishing" in status_document.content
    assert "公開 API には破壊的変更を加えず" in status_document.content
    assert "メジャーバージョンへ移行する" in status_document.content
    assert "Beta" in status_document.content
    assert CONTEXT["project"]["version"] in status_document.content
    assert "Project Status 専用規定体ではなく" in status_document.content


def test_repository_changelog_dogfoods_list_fields() -> None:
    result = document_system.validate(changelog_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = DocumentMarkdownRealizer(CONTEXT)
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    documents = realizer.realize(result.view)
    assert len(documents) == 1
    changelog = documents[0]
    assert changelog.filename == "CHANGELOG.md"
    assert "## V0_3_5" in changelog.content
    assert "version: 0.3.5" in changelog.content
    assert "## V0_3_3" in changelog.content
    assert "## V0_3_2" in changelog.content
    assert "version: 0.3.2" in changelog.content
    assert 'merge_policy="forbidden"' in changelog.content
    assert "## V0_3_1" in changelog.content
    assert "version: 0.3.1" in changelog.content
    assert "## V0_3_0" in changelog.content
    assert "version: 0.3.0" in changelog.content
    assert "Added:\n\n- `shikumi_devdoc.norms.document`" in changelog.content
    assert (
        "Specification、API Reference、Project Status、CHANGELOG の専用規定体"
        in changelog.content
    )


def test_repository_vocabulary_uses_stable_term_identifiers() -> None:
    identifiers = [
        name
        for name, value in vars(TERMS).items()
        if isinstance(value, type) and name.startswith("TERM_")
    ]
    assert identifiers == [f"TERM_{index:03d}" for index in range(1, 18)]
    assert not hasattr(TERMS, "CANONICAL_SOURCE")


def test_repository_specification_dogfoods_vocabulary_terms() -> None:
    result = document_system.validate(specification, placement=())
    assert result.is_valid, result.diagnostics

    core_boundary = next(
        item for item in result.view.entities if item.subject is CORE_SPEC.CORE_004
    )
    from shikumi_devdoc.norms._document import template_reference_bindings

    bindings, ambiguous = template_reference_bindings(core_boundary)
    assert not ambiguous
    assert bindings["TERM_001"] is TERMS.TERM_001
    assert bindings["TERM_002"] is TERMS.TERM_002
    assert bindings["TERM_005"] is TERMS.TERM_005


def test_repository_specification_dogfoods_generic_documents() -> None:
    result = document_system.validate(specification, placement=())
    assert result.is_valid, result.diagnostics

    realizer = DocumentMarkdownRealizer(CONTEXT)
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    documents = realizer.realize(result.view)
    by_name = {document.filename: document.content for document in documents}

    assert set(by_name) == {
        "api-reference.md",
        "cli.md",
        "core.md",
        "distribution.md",
        "document.md",
        "field-presentations.md",
        "rendering.md",
        "specification.md",
        "vocabulary.md",
    }

    index_realizer = IndexMarkdownRealizer(
        CONTEXT, title="shikumi-devdoc Specification"
    )
    index_check = index_realizer.check(result.view)
    assert index_check.is_realizable, index_check.diagnostics
    index = index_realizer.realize(result.view)
    assert index.filename == "INDEX.md"
    assert "[Core](core.md)" in index.content
    assert "[Command-line interface](cli.md)" in index.content

    structured = by_name["specification.md"]
    assert "## SPEC_005" in structured
    assert "level: MUST" in structured
    assert "condition: Markdown へ実現する場合。" in structured
    assert "### level" not in structured
    assert "## level" not in structured

    field_presentations = by_name["field-presentations.md"]
    assert "## FIELD_003" in field_presentations
    assert "`list_field()`" in field_presentations
    assert "`test_target_field()`" in field_presentations
    assert "`table_field()`" in field_presentations
    assert "`prose_field()`" in field_presentations

    rendering = by_name["rendering.md"]
    assert "related: [SPEC_003](specification.md#spec_003)" in rendering
    assert "### Related" not in rendering


def test_repository_api_reference_dogfoods_standard_field_set() -> None:
    result = document_system.validate(api_reference, placement=())
    assert result.is_valid, result.diagnostics

    realizer = DocumentMarkdownRealizer(CONTEXT)
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    documents = realizer.realize(result.view)
    by_name = {document.filename: document.content for document in documents}

    assert set(by_name) == {
        "cli.md",
        "context.md",
        "core.md",
        "norms.md",
        "fields.md",
        "realizers.md",
    }

    index_realizer = IndexMarkdownRealizer(
        CONTEXT, title="shikumi-devdoc API Reference"
    )
    index_check = index_realizer.check(result.view)
    assert index_check.is_realizable, index_check.diagnostics
    index = index_realizer.realize(result.view)
    assert index.filename == "INDEX.md"
    assert "[Core](core.md)" in index.content
    assert "[Realizers](realizers.md)" in index.content

    context = by_name["context.md"]
    assert "## Context" in context
    assert "### resolve" in context
    assert "input: key [str]" in context
    assert "output: output [str]" in context
    assert "#### Inputs" not in context

    corpus = "\n".join(by_name.values())
    for path in _public_paths(public_fields, "shikumi_devdoc.fields"):
        assert f"name: {path}" in corpus or path in corpus
    for path in _public_paths(public_norms, "shikumi_devdoc.norms"):
        assert f"name: {path}" in corpus
    for path in _public_paths(public_realizers, "shikumi_devdoc.realizers"):
        assert f"name: {path}" in corpus
    for name in ("Context", "ContextError", "UnknownContextKeyError"):
        assert f"name: shikumi_devdoc.{name}" in corpus


def test_repository_publishes_translated_dogfood_documents() -> None:
    expected = [
        Path("STATUS.md"),
        *(
            Path("docs/authoring_guide") / name
            for name in (
                "INDEX.md",
                "overview.md",
                "readme.md",
                "getting-started.md",
                "configuration-guide.md",
                "cli-documentation.md",
                "specification.md",
                "api-reference.md",
                "changelog.md",
                "glossary.md",
                "project-status.md",
                "collections.md",
                "advanced-authoring.md",
                "llm-workflow.md",
            )
        ),
        *(
            Path("docs/specification") / name
            for name in (
                "INDEX.md",
                "core.md",
                "document.md",
                "vocabulary.md",
                "field-presentations.md",
                "specification.md",
                "api-reference.md",
                "rendering.md",
                "cli.md",
                "distribution.md",
            )
        ),
        *(
            Path("docs/api") / name
            for name in (
                "INDEX.md",
                "core.md",
                "context.md",
                "norms.md",
                "fields.md",
                "realizers.md",
                "cli.md",
            )
        ),
    ]
    for path in expected:
        content = path.read_text(encoding="utf-8")
        assert content.startswith("# ")
        assert "この文書は自動生成されています" not in content
        assert "shikumi-devdoc:translation-metadata" not in content


def test_published_api_corpus_covers_public_namespaces() -> None:
    corpus = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(Path("docs/api").glob("*.md"))
    )
    for path in _public_paths(public_fields, "shikumi_devdoc.fields"):
        assert path in corpus
    for path in _public_paths(public_norms, "shikumi_devdoc.norms"):
        assert path in corpus
    for path in _public_paths(public_realizers, "shikumi_devdoc.realizers"):
        assert path in corpus
    for name in ("Context", "ContextError", "UnknownContextKeyError"):
        assert f"shikumi_devdoc.{name}" in corpus


def test_published_fragment_links_resolve_to_rendered_heading_contract() -> None:
    from shikumi_devdoc.realizers._markdown_heading import heading_fragment

    markdown_files = [Path("README.md"), Path("STATUS.md"), Path("CHANGELOG.md")]
    markdown_files.extend(sorted(Path("docs").rglob("*.md")))
    heading_pattern = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    headings = {
        path.resolve(): {
            heading_fragment(match.group(1))
            for match in heading_pattern.finditer(path.read_text(encoding="utf-8"))
        }
        for path in markdown_files
    }

    checked = 0
    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        assert "<a id=" not in text
        for match in link_pattern.finditer(text):
            destination = match.group(1)
            if (
                destination.startswith(("http://", "https://", "mailto:"))
                or "#" not in destination
            ):
                continue
            path_text, fragment = destination.split("#", 1)
            target = (
                (source.parent / path_text).resolve() if path_text else source.resolve()
            )
            if target not in headings:
                continue
            checked += 1
            assert fragment in headings[target], (source, destination)

    assert checked > 0


def test_publication_rewrites_fragment_when_published_heading_changes() -> None:
    result = document_system.validate(api_reference, placement=())
    assert result.is_valid, result.diagnostics
    canonical = {
        document.filename: document.content
        for document in DocumentMarkdownRealizer(CONTEXT).realize(result.view)
    }

    # The realizer derives canonical-document topology from source provenance
    # plus declared filenames, without inspecting realization output directories.
    assert "[CORE_001](../specification/core.md#core_001)" in canonical["norms.md"]

    # This repository preserves that logical directory relationship at publication,
    # while translating the visible heading and therefore rewriting the fragment.
    published = Path("docs/api/norms.md").read_text(encoding="utf-8")
    assert "[CORE_001](../specification/core.md#core_001-canonical-source)" in published
    target = Path("docs/specification/core.md").read_text(encoding="utf-8")
    assert "## CORE_001 Canonical source" in target
    assert "<a id=" not in target
