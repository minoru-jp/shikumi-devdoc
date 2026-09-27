import ast
from inspect import cleandoc
from textwrap import dedent
from pathlib import Path

from devdocs.canonical_sources.authoring_guide import advanced_authoring as authoring_advanced_source
from devdocs.canonical_sources.authoring_guide import changelog_guide as authoring_changelog_source
from devdocs.canonical_sources.authoring_guide import glossary_guide as authoring_glossary_source
from devdocs.canonical_sources.readme import canonical as readme_source
from shikumi_devdoc.norms._document import DocumentField, FieldPresentation, FieldValue
from shikumi_devdoc.norms.document import system as document_system
from shikumi_devdoc.norms.vocabulary import system as vocabulary_system
from shikumi_devdoc.realizers.document import MarkdownRealizer
from tests.examples import (
    authoring_external_vocabulary,
    authoring_lifecycle,
    authoring_vocabulary,
    authoring_vocabulary_reference,
    authoring_test_target,
    readme_quickstart,
)


ROOT = Path(__file__).resolve().parent


def _source_snippet(path: Path, name: str) -> str:
    start = f"# DOC-SNIPPET {name} START"
    end = f"# DOC-SNIPPET {name} END"
    lines = path.read_text(encoding="utf-8").splitlines()
    start_index = lines.index(start) + 1 if start in lines else next(
        index + 1 for index, line in enumerate(lines) if line.strip() == start
    )
    end_index = lines.index(end) if end in lines else next(
        index for index, line in enumerate(lines) if line.strip() == end
    )
    return dedent("\n".join(lines[start_index:end_index])).strip()


def _same_python_syntax(left: str, right: str) -> bool:
    return ast.dump(ast.parse(left), include_attributes=False) == ast.dump(
        ast.parse(right), include_attributes=False
    )


def _test_target_field_value(module, subject: type[object], binding_name: str) -> str:
    result = document_system.validate(module, placement=())
    assert result.is_valid, result.diagnostics
    item = next(entity for entity in result.view.entities if entity.subject is subject)
    values = [
        value
        for value in item.values(DocumentField)
        if isinstance(value, FieldValue) and value.binding_name == binding_name
    ]
    assert len(values) == 1
    assert values[0].presentation is FieldPresentation.TEST_TARGET
    assert isinstance(values[0].value, str)
    return cleandoc(values[0].value)


def test_readme_minimal_source_is_the_tested_example_module() -> None:
    documented = _test_target_field_value(
        readme_source,
        readme_source.SECTION_001.SECTION_003,
        "minimal_source",
    )
    executable = _source_snippet(
        ROOT / "examples" / "readme_quickstart.py",
        "readme-minimal-source",
    )
    assert _same_python_syntax(documented, executable)

    result = document_system.validate(readme_quickstart, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer().realize(result.view)[0]
    assert rendered.filename == "example.md"
    assert rendered.content == (
        "# Example\n\n"
        "## Introduction\n\n"
        "Hello from shikumi-devdoc.\n"
    )


def test_authoring_vocabulary_definition_is_the_tested_example_module() -> None:
    documented = _test_target_field_value(
        authoring_glossary_source,
        authoring_glossary_source.AUTHORING_GUIDE_PART.SECTION_002,
        "vocabulary_definition_example",
    )
    executable = _source_snippet(
        ROOT / "examples" / "authoring_vocabulary.py",
        "authoring-vocabulary-definition",
    )
    assert _same_python_syntax(documented, executable)

    result = vocabulary_system.validate(authoring_vocabulary, placement=())
    assert result.is_valid, result.diagnostics


def test_authoring_external_vocabulary_snippet_is_covered_by_executable_module() -> None:
    documented = _test_target_field_value(
        authoring_glossary_source,
        authoring_glossary_source.AUTHORING_GUIDE_PART.SECTION_004,
        "external_vocabulary_merge_example",
    )
    executable = _source_snippet(
        ROOT / "examples" / "authoring_external_vocabulary.py",
        "authoring-external-vocabulary",
    )
    assert _same_python_syntax(documented, executable)

    result = document_system.validate(authoring_external_vocabulary, placement=())
    assert result.is_valid, result.diagnostics
    content = MarkdownRealizer().realize(result.view)[0].content
    assert "The shared name is framework term." in content


def test_authoring_vocabulary_reference_snippet_is_covered_by_executable_module() -> None:
    documented = _test_target_field_value(
        authoring_glossary_source,
        authoring_glossary_source.AUTHORING_GUIDE_PART.SECTION_003,
        "vocabulary_reference_example",
    )
    executable = _source_snippet(
        ROOT / "examples" / "authoring_vocabulary_reference.py",
        "authoring-vocabulary-reference",
    )
    assert _same_python_syntax(documented, executable)

    result = document_system.validate(authoring_vocabulary_reference, placement=())
    assert result.is_valid, result.diagnostics
    content = MarkdownRealizer().realize(result.view)[0].content
    assert "この文書の正本は canonical source である。" in content


def test_authoring_test_target_field_snippet_is_covered_by_executable_module() -> None:
    documented = _test_target_field_value(
        authoring_advanced_source,
        authoring_advanced_source.AUTHORING_GUIDE_PART.SECTION_006,
        "documented_snippet",
    )
    executable = _source_snippet(
        ROOT / "examples" / "authoring_test_target.py",
        "authoring-test-target-field",
    )
    assert _same_python_syntax(documented, executable)

    result = document_system.validate(authoring_test_target, placement=())
    assert result.is_valid, result.diagnostics
    rendered = MarkdownRealizer().realize(result.view)[0].content
    assert '```python\nprint("hello")\n```' in rendered
    assert 'example:' not in rendered


def test_authoring_lifecycle_snippet_is_covered_by_executable_module() -> None:
    documented = _test_target_field_value(
        authoring_changelog_source,
        authoring_changelog_source.AUTHORING_GUIDE_PART.SECTION_004,
        "lifecycle_example",
    )
    executable = _source_snippet(
        ROOT / "examples" / "authoring_lifecycle.py",
        "authoring-lifecycle",
    )
    assert _same_python_syntax(documented, executable)

    result = document_system.validate(authoring_lifecycle, placement=())
    assert result.is_valid, result.diagnostics
    content = MarkdownRealizer().realize(result.view)[0].content
    assert "introduced: 0.2.0" in content
    assert "deprecated: 0.4.0" in content
    assert "replacement: new_api" in content
    assert "Replace `old_api` with `new_api`" in content
