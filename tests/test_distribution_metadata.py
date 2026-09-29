from pathlib import Path
import tomllib


def _pyproject() -> dict:
    return tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))


def test_test_extra_declares_pytest() -> None:
    project = _pyproject()["project"]
    assert project["optional-dependencies"]["test"] == ["pytest>=8.0"]


def test_sdist_uses_release_source_snapshot_policy() -> None:
    sdist = _pyproject()["tool"]["hatch"]["build"]["targets"]["sdist"]
    assert "include" not in sdist
    assert sdist["exclude"] == ["/.github"]

    for path in ("src", "tests", "devdocs", "docs", "scripts"):
        assert Path(path).exists()


def test_runtime_dependency_targets_shikumi_0_2_or_newer() -> None:
    project = _pyproject()["project"]
    assert project["dependencies"] == ["shikumi>=0.2.0"]


def test_project_urls_point_to_public_repository() -> None:
    urls = _pyproject()["project"]["urls"]
    assert urls == {
        "Repository": "https://github.com/minoru-jp/shikumi-devdoc",
        "Documentation": "https://github.com/minoru-jp/shikumi-devdoc#documentation",
        "Changelog": "https://github.com/minoru-jp/shikumi-devdoc/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/minoru-jp/shikumi-devdoc/issues",
    }
