from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import venv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

REQUIRED_WHEEL_SUFFIXES = {
    "shikumi_devdoc/__init__.py",
    "shikumi_devdoc/cli.py",
    "shikumi_devdoc/resources/devdocs/canonical_sources/status/canonical.py",
    "shikumi_devdoc/resources/devdocs/canonical_documents/STATUS.md",
    "shikumi_devdoc/resources/published_docs/README.md",
    "shikumi_devdoc/resources/published_docs/STATUS.md",
    "shikumi_devdoc/resources/published_docs/CHANGELOG.md",
    "shikumi_devdoc/resources/published_docs/docs/authoring_guide/INDEX.md",
    "shikumi_devdoc/resources/published_docs/docs/specification/INDEX.md",
    "shikumi_devdoc/resources/published_docs/docs/api/INDEX.md",
}

REQUIRED_SDIST_SUFFIXES = {
    "src/shikumi_devdoc/__init__.py",
    "tests/test_dogfood.py",
    "devdocs/canonical_sources/status/canonical.py",
    "devdocs/canonical_documents/STATUS.md",
    "docs/authoring_guide/INDEX.md",
    "docs/specification/INDEX.md",
    "docs/api/INDEX.md",
    "README.md",
    "STATUS.md",
    "CHANGELOG.md",
    "LICENSE",
    "pyproject.toml",
    "scripts/check_dist.py",
}

FORBIDDEN_ARCHIVE_PARTS = {".github", "__pycache__", ".pytest_cache"}


def _run(args: list[str | os.PathLike[str]], *, env: dict[str, str] | None = None) -> None:
    command = [os.fspath(arg) for arg in args]
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def _clean_dist() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()


def _build() -> tuple[Path, Path]:
    _clean_dist()
    _run([sys.executable, "-m", "build"])
    wheels = sorted(DIST.glob("*.whl"))
    sdists = sorted(DIST.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise SystemExit(f"expected one wheel and one sdist, found {wheels=} {sdists=}")
    return wheels[0], sdists[0]


def _assert_no_forbidden_parts(names: list[str], *, archive: Path) -> None:
    bad = [name for name in names if FORBIDDEN_ARCHIVE_PARTS.intersection(Path(name).parts)]
    if bad:
        raise SystemExit(f"forbidden paths in {archive.name}: {bad[:20]}")


def _assert_suffixes(names: list[str], required: set[str], *, archive: Path) -> None:
    missing = [suffix for suffix in sorted(required) if not any(name.endswith(suffix) for name in names)]
    if missing:
        raise SystemExit(f"missing required paths in {archive.name}: {missing}")


def _check_wheel(wheel: Path) -> None:
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        _assert_no_forbidden_parts(names, archive=wheel)
        _assert_suffixes(names, REQUIRED_WHEEL_SUFFIXES, archive=wheel)

        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise SystemExit(f"expected one METADATA file in {wheel.name}, found {metadata_names}")
        metadata = archive.read(metadata_names[0]).decode("utf-8")
        requirements = [
            line.removeprefix("Requires-Dist: ").strip()
            for line in metadata.splitlines()
            if line.startswith("Requires-Dist: ")
        ]
        if "shikumi>=0.2.0" not in requirements:
            raise SystemExit(
                f"wheel metadata must contain exactly shikumi>=0.2.0; found {requirements}"
            )


def _check_sdist(sdist: Path) -> None:
    with tarfile.open(sdist, "r:gz") as archive:
        names = archive.getnames()
        _assert_no_forbidden_parts(names, archive=sdist)
        _assert_suffixes(names, REQUIRED_SDIST_SUFFIXES, archive=sdist)


def _venv_paths(directory: Path) -> tuple[Path, Path]:
    if os.name == "nt":
        bin_dir = directory / "Scripts"
        return bin_dir / "python.exe", bin_dir / "shikumi-devdoc.exe"
    bin_dir = directory / "bin"
    return bin_dir / "python", bin_dir / "shikumi-devdoc"


def _install_artifact(
    artifact: Path,
    *,
    environment: Path,
    shikumi_source: Path | None,
) -> tuple[Path, Path]:
    venv.EnvBuilder(with_pip=True).create(environment)
    python, cli = _venv_paths(environment)

    if shikumi_source is not None:
        _run([python, "-m", "pip", "install", shikumi_source])
        _run([python, "-m", "pip", "install", "--no-deps", artifact])
    else:
        _run([python, "-m", "pip", "install", artifact])

    _run([python, "-m", "pip", "check"])
    _run([cli, "--help"])
    return python, cli


def _check_installed_wheel(python: Path, cli: Path, *, work: Path) -> None:
    code = r'''
from importlib.resources import files

root = files("shikumi_devdoc")
expected = (
    "resources/devdocs/canonical_sources",
    "resources/devdocs/canonical_documents",
    "resources/published_docs/README.md",
    "resources/published_docs/STATUS.md",
    "resources/published_docs/CHANGELOG.md",
    "resources/published_docs/docs/authoring_guide/INDEX.md",
    "resources/published_docs/docs/specification/INDEX.md",
    "resources/published_docs/docs/api/INDEX.md",
)
missing = []
for path in expected:
    item = root.joinpath(*path.split("/"))
    if not item.is_file() and not item.is_dir():
        missing.append(path)
if missing:
    raise SystemExit(f"missing wheel resources: {missing}")
'''
    _run([python, "-c", code])

    out = work / "dogfood"
    out.mkdir()
    context = (ROOT / "devdocs/config/context.json").read_text(encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.fspath(ROOT)

    commands = [
        [cli, "render", "glossary", "devdocs.canonical_sources.vocabulary.canonical", "-o", out / "GLOSSARY.md", "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "document", "devdocs.canonical_sources.readme.canonical", "-o", out / "readme", "--context", context, "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "document", "devdocs.canonical_sources.authoring_guide", "-o", out / "authoring_guide", "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "index", "devdocs.canonical_sources.authoring_guide", "-o", out / "authoring_guide", "--index-title", "shikumi-devdoc Authoring Guide", "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "document", "devdocs.canonical_sources.workspace.canonical", "-o", out / "devdocs", "--notice", "devdocs/config/notice.toml"],
        [cli, "render", "document", "devdocs.canonical_sources.status.canonical", "-o", out / "status", "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "document", "devdocs.canonical_sources.changelog.canonical", "-o", out / "changelog", "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "document", "devdocs.canonical_sources.specification", "-o", out / "specification", "--context", context, "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "index", "devdocs.canonical_sources.specification", "-o", out / "specification", "--context", context, "--index-title", "shikumi-devdoc Specification", "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "document", "devdocs.canonical_sources.api_reference", "-o", out / "api", "--context", context, "--notice", "devdocs/config/notice.toml", "--translation-source"],
        [cli, "render", "index", "devdocs.canonical_sources.api_reference", "-o", out / "api", "--context", context, "--index-title", "shikumi-devdoc API Reference", "--notice", "devdocs/config/notice.toml", "--translation-source"],
    ]
    for command in commands:
        command = [os.fspath(part) for part in command]
        print("+", " ".join(command), flush=True)
        subprocess.run(command, cwd=ROOT, env=env, check=True)

    expected_outputs = (
        out / "GLOSSARY.md",
        out / "readme/README.md",
        out / "authoring_guide/INDEX.md",
        out / "devdocs/README.md",
        out / "status/STATUS.md",
        out / "changelog/CHANGELOG.md",
        out / "specification/INDEX.md",
        out / "api/INDEX.md",
    )
    missing = [path for path in expected_outputs if not path.is_file() or path.stat().st_size == 0]
    if missing:
        raise SystemExit(f"dogfood smoke output missing or empty: {missing}")


def _installed_smoke(wheel: Path, sdist: Path, *, shikumi_source: Path | None) -> None:
    with tempfile.TemporaryDirectory(prefix="shikumi-devdoc-release-") as temp:
        temp_root = Path(temp)
        wheel_python, wheel_cli = _install_artifact(
            wheel,
            environment=temp_root / "wheel-env",
            shikumi_source=shikumi_source,
        )
        _check_installed_wheel(wheel_python, wheel_cli, work=temp_root)

        sdist_python, _ = _install_artifact(
            sdist,
            environment=temp_root / "sdist-env",
            shikumi_source=shikumi_source,
        )
        _run([sdist_python, "-c", "import shikumi_devdoc"])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build and locally verify the shikumi-devdoc release distributions."
    )
    parser.add_argument(
        "--shikumi-source",
        type=Path,
        help="Install Shikumi from this source tree before smoke-testing artifacts. Useful before the required Shikumi version is on PyPI.",
    )
    parser.add_argument(
        "--archive-only",
        action="store_true",
        help="Build and inspect wheel/sdist contents without creating installation smoke-test environments.",
    )
    args = parser.parse_args()

    shikumi_source = args.shikumi_source.resolve() if args.shikumi_source else None
    if shikumi_source is not None and not (shikumi_source / "pyproject.toml").is_file():
        raise SystemExit(f"not a Python project: {shikumi_source}")

    wheel, sdist = _build()
    _check_wheel(wheel)
    _check_sdist(sdist)
    if not args.archive_only:
        _installed_smoke(wheel, sdist, shikumi_source=shikumi_source)

    print(f"release distributions verified: {wheel.name}, {sdist.name}")


if __name__ == "__main__":
    main()
