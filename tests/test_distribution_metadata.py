from pathlib import Path
import tomllib


def _pyproject() -> dict:
    return tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))


def test_test_extra_declares_pytest() -> None:
    project = _pyproject()["project"]
    assert project["optional-dependencies"]["test"] == ["pytest>=8.0"]


def test_sdist_contains_test_sources_and_build_metadata() -> None:
    sdist = _pyproject()["tool"]["hatch"]["build"]["targets"]["sdist"]
    assert "/tests" in sdist["include"]
    assert "/pyproject.toml" in sdist["include"]


def test_runtime_dependency_targets_shikumi_0_2_or_newer() -> None:
    project = _pyproject()["project"]
    assert project["dependencies"] == ["shikumi>=0.2.0"]
