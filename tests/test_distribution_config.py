from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"


def _project_config() -> dict[str, object]:
    with PYPROJECT.open("rb") as stream:
        return tomllib.load(stream)


def test_wheel_distributes_reference_and_published_document_resources() -> None:
    config = _project_config()
    force_include = config["tool"]["hatch"]["build"]["targets"]["wheel"]["force-include"]
    assert force_include == {
        "devdocs": "shikumi_devdoc/resources/devdocs",
        "README.md": "shikumi_devdoc/resources/published_docs/README.md",
        "STATUS.md": "shikumi_devdoc/resources/published_docs/STATUS.md",
        "CHANGELOG.md": "shikumi_devdoc/resources/published_docs/CHANGELOG.md",
        "docs": "shikumi_devdoc/resources/published_docs/docs",
    }

    for source in force_include:
        assert (ROOT / source).exists()


def test_license_uses_distribution_metadata_not_document_resource_copy() -> None:
    config = _project_config()
    project = config["project"]
    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE"]

    force_include = config["tool"]["hatch"]["build"]["targets"]["wheel"]["force-include"]
    assert "LICENSE" not in force_include
