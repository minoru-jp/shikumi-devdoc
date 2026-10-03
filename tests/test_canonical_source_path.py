from pathlib import Path

from shikumi_devdoc.norms._common import (
    CanonicalDocumentPath,
    _document_path_for_source,
    _source_path_for_module,
    _source_path_for_subject,
)
from tests.fixtures import canonical_document_package
from tests.fixtures.canonical_document_package.canonical import DOCUMENT

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_source_path_is_independent_of_working_directory(monkeypatch) -> None:
    monkeypatch.chdir(ROOT.parent)

    assert _source_path_for_subject(DOCUMENT) == (
        "tests/fixtures/canonical_document_package/canonical.py"
    )


def test_package_source_path_uses_init_module_structure() -> None:
    assert _source_path_for_module(canonical_document_package) == (
        "tests/fixtures/canonical_document_package/__init__.py"
    )


def test_logical_document_path_uses_source_parent_and_declared_filename() -> None:
    assert (
        _document_path_for_source(
            "tests/fixtures/logical_reference_target/document.py",
            "target.md",
        )
        == "tests/fixtures/logical_reference_target/target.md"
    )


def test_canonical_document_root_carries_logical_document_path() -> None:
    from shikumi import information_of

    from tests.fixtures.logical_reference_target.document import TARGET

    values = tuple(
        record.value
        for record in information_of(TARGET)
        if record.type is CanonicalDocumentPath
    )
    assert values == ("tests/fixtures/logical_reference_target/target.md",)
