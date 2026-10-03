from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "tests/mypy_recipe/pyproject.toml"
PACKAGE = ROOT / "tests/mypy_recipe/your_project/devdocs/canonical_sources"
POSITIVE = PACKAGE / "authoring.py"
NEGATIVE = PACKAGE / "non_misc_error.py"


def _run(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "--config-file",
            str(CONFIG),
            str(path),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def main() -> None:
    positive = _run(POSITIVE)
    if positive.returncode != 0:
        print(positive.stdout, end="", file=sys.stderr)
        raise SystemExit("documented mypy override did not accept the @= fixture")

    negative = _run(NEGATIVE)
    if negative.returncode == 0:
        print(negative.stdout, end="", file=sys.stderr)
        raise SystemExit("mypy override unexpectedly hid a non-misc type error")
    if "[arg-type]" not in negative.stdout:
        print(negative.stdout, end="", file=sys.stderr)
        raise SystemExit(
            "mypy negative fixture did not report the expected arg-type error"
        )

    print("mypy override recipe accepts @= and preserves non-misc diagnostics")


if __name__ == "__main__":
    main()
