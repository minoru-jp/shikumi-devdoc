from __future__ import annotations

import importlib.util
from pathlib import Path

from shikumi import information_of
from tests.fixtures import vocabulary_source
from shikumi_devdoc.norms.common import VocabularyReference, vocabulary_refs
from shikumi_devdoc.norms.vocabulary import vocabulary_system
from shikumi_devdoc.realizers.vocabulary_reference_python import PythonReferenceModuleRealizer


def _load_generated_terms(path: Path):
    spec = importlib.util.spec_from_file_location("generated_terms", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_python_reference_module_contains_term_names_and_definitions(tmp_path: Path) -> None:
    result = vocabulary_system.validate(vocabulary_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = PythonReferenceModuleRealizer("tests.fixtures.vocabulary_source")
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)
    assert "class TERM_1:" in rendered
    assert "Widget" in rendered
    assert "A reusable widget." in rendered

    path = tmp_path / "terms.py"
    path.write_text(rendered, encoding="utf-8")
    module = _load_generated_terms(path)

    assert module.__shikumi_devdoc_vocabulary_source__ is vocabulary_source
    assert module.TERM_1.__doc__ == "Widget\n\nA reusable widget."
    assert module.TERM_2.__doc__ == "InternalName\n\nAn implementation-only identifier."


def test_generated_term_proxy_preserves_canonical_reference_identity(tmp_path: Path) -> None:
    view = vocabulary_system.view(vocabulary_source, placement=())
    path = tmp_path / "terms.py"
    path.write_text(
        PythonReferenceModuleRealizer("tests.fixtures.vocabulary_source").realize(view),
        encoding="utf-8",
    )
    terms = _load_generated_terms(path)

    class DESCRIPTION:
        vocabulary_refs @= (terms.TERM_1, terms.TERM_2)

    references = [
        information.value
        for information in information_of(DESCRIPTION)
        if information.type is VocabularyReference
    ]
    assert references == [
        vocabulary_source.VOCABULARY.TERM_1,
        vocabulary_source.VOCABULARY.TERM_2,
    ]


def test_python_reference_module_includes_alias_and_deprecation_notes() -> None:
    from tests.fixtures import vocabulary_lifecycle

    result = vocabulary_system.validate(vocabulary_lifecycle, placement=())
    assert result.is_valid, result.diagnostics

    rendered = PythonReferenceModuleRealizer(
        "tests.fixtures.vocabulary_lifecycle"
    ).realize(result.view)

    assert "Aliases: Component, UI Widget" in rendered
    assert "Deprecated. Use Widget instead." in rendered
