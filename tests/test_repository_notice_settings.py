from pathlib import Path
import json
import tomllib


ROOT = Path(__file__).resolve().parents[1]
NOTICE = ROOT / "devdocs/config/notice.toml"
CONTEXT = ROOT / "devdocs/config/context.json"


def _notice() -> dict[str, object]:
    with NOTICE.open("rb") as stream:
        return tomllib.load(stream)


def test_repository_notice_is_single_operational_content() -> None:
    config = _notice()
    content = config["notice"]["content"]
    assert "{canonical_source}" in content
    assert "canonical document" in content
    assert "公開文書作成方針" in content
    assert "published document には含めない" in content
    assert set(config) == {"notice"}


def test_repository_realization_context_is_explicit_json() -> None:
    context = json.loads(CONTEXT.read_text(encoding="utf-8"))
    assert context == {
        "project": {
            "name": "shikumi-devdoc",
            "version": "0.3.2",
            "requires-python": ">=3.11",
        }
    }


def test_canonical_documents_receive_repository_notice() -> None:
    paths = [
        ROOT / "devdocs/canonical_documents/README.md",
        ROOT / "devdocs/canonical_documents/devdocs/README.md",
        *sorted((ROOT / "devdocs/canonical_documents/changelog").glob("*.md")),
    ]
    assert [path.name for path in paths[2:]] == ["CHANGELOG.md"]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert text.lstrip().startswith("<!--")
        assert "公開文書作成方針" in text.split("-->", 1)[0]


def test_public_documents_do_not_start_with_operational_comment() -> None:
    for path in (ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "devdocs/README.md"):
        text = path.read_text(encoding="utf-8")
        assert not text.lstrip().startswith("<!--")


def test_devdocs_workspace_has_explicit_authoring_boundaries() -> None:
    assert (ROOT / "devdocs/canonical_sources").is_dir()
    assert not (ROOT / "devdocs/fields").exists()
    assert (ROOT / "devdocs/config").is_dir()
    assert (ROOT / "devdocs/canonical_documents").is_dir()
    assert not (ROOT / "_internal").exists()
    assert not (ROOT / "devdocs/intermediate_documents").exists()
    assert not (ROOT / "devdocs/document_source").exists()
    assert not (ROOT / "devdocs/document_build").exists()

    text = (ROOT / "devdocs/README.md").read_text(encoding="utf-8")
    assert "canonical_sources/" in text
    assert "fields/terms.py" not in text
    assert "canonical_documents/" in text
    assert "config/context.json" in text
    assert "config/notice.toml" in text
