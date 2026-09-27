from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "_internal/document_source/notice.toml"


def _config() -> dict[str, object]:
    with CONFIG.open("rb") as stream:
        return tomllib.load(stream)


def test_repository_notice_is_single_operational_content() -> None:
    config = _config()
    content = config["notice"]["content"]
    assert "{canonical_source}" in content
    assert "公開文書作成方針" in content
    assert "公開文書には含めない" in content
    assert set(config) == {"notice"}


def test_intermediate_documents_receive_repository_notice() -> None:
    for name in ("README.md", "CHANGELOG.md"):
        text = (ROOT / "_internal/document_build/ja" / name).read_text(encoding="utf-8")
        assert text.lstrip().startswith("<!--")
        assert "公開文書作成方針" in text.split("-->", 1)[0]


def test_public_documents_do_not_start_with_operational_comment() -> None:
    for name in ("README.md", "CHANGELOG.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert not text.lstrip().startswith("<!--")


def test_repository_context_is_not_persisted_as_a_file() -> None:
    assert not (ROOT / "_internal/document_source/context.toml").exists()


def test_repository_directory_readme_describes_explicit_inputs() -> None:
    text = (ROOT / "_internal/document_source/README.md").read_text(encoding="utf-8")
    assert "--notice" in text
    assert "--context" in text
    assert "JSON 文字列" in text
    assert "文書ソースとは" not in text
