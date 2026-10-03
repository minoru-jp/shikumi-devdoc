import json
import tomllib
from pathlib import Path


def _pyproject() -> dict:
    return tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))


def test_test_extra_declares_pytest() -> None:
    project = _pyproject()["project"]
    assert project["optional-dependencies"]["test"] == ["pytest>=8.0"]


def test_lint_extra_declares_pinned_ruff() -> None:
    project = _pyproject()["project"]
    assert project["optional-dependencies"]["lint"] == ["ruff==0.16.10"]


def test_typecheck_extra_declares_pinned_checkers() -> None:
    project = _pyproject()["project"]
    assert project["optional-dependencies"]["typecheck"] == [
        "basedpyright==1.40.1",
        "mypy==2.4.0",
    ]


def test_ruff_configuration_matches_project_policy() -> None:
    config = _pyproject()["tool"]["ruff"]
    assert config == {
        "target-version": "py311",
        "lint": {"preview": False},
    }


def test_basedpyright_configuration_matches_project_policy() -> None:
    config = _pyproject()["tool"]["basedpyright"]
    assert config == {
        "include": ["src/shikumi_devdoc"],
        "pythonVersion": "3.11",
        "reportUnnecessaryIsInstance": False,
        "reportImplicitStringConcatenation": False,
        "reportExplicitAny": False,
        "reportPrivateUsage": False,
        "reportImplicitOverride": False,
    }


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


def test_consumer_typing_contract_checks_dogfood_sources() -> None:
    typing_config = json.loads(
        Path("tests/typing/pyrightconfig.json").read_text(encoding="utf-8")
    )
    assert typing_config == {
        "include": [".", "../../devdocs/canonical_sources", "../examples"],
        "extraPaths": ["../..", "../../src"],
        "pythonVersion": "3.11",
        "typeCheckingMode": "standard",
        "enableTypeIgnoreComments": False,
        "reportUnnecessaryTypeIgnoreComment": "error",
    }


def test_shared_quality_gate_runs_consumer_typing_contract() -> None:
    workflow = Path(".github/workflows/checks.yml").read_text(encoding="utf-8")
    assert "run: basedpyright -p tests/typing" in workflow
    assert "run: python scripts/check_mypy_recipe.py" in workflow


def test_documented_mypy_recipe_disables_only_misc_by_code() -> None:
    recipe = tomllib.loads(
        Path("tests/mypy_recipe/pyproject.toml").read_text(encoding="utf-8")
    )
    override = recipe["tool"]["mypy"]["overrides"]
    assert override == [
        {
            "module": ["your_project.devdocs.canonical_sources.*"],
            "disable_error_code": ["misc"],
        }
    ]


def test_release_build_requires_shared_checks() -> None:
    workflow = Path(".github/workflows/release.yml").read_text(encoding="utf-8")
    build = workflow.split("  build:\n", 1)[1].split("  publish:\n", 1)[0]
    assert "    needs: checks\n" in build


def test_repository_declares_lf_text_policy() -> None:
    attributes = Path(".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "*.py text eol=lf" in attributes
    assert "*.toml text eol=lf" in attributes
    assert "*.yml text eol=lf" in attributes
    assert "*.yaml text eol=lf" in attributes
    assert "*.md text eol=lf" in attributes
    assert "*.json text eol=lf" in attributes
