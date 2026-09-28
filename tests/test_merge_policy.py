import os
from pathlib import Path
import subprocess
import sys
import warnings

import pytest
from shikumi import information_of

from shikumi_devdoc.norms._common import CanonicalMergePolicy, MergePolicy
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import system
from shikumi_devdoc.realizers.document_markdown import MarkdownRealizer


CONTEXT = {"PROJECT": {"name": "Example", "version": "1.2.3"}}


def _policy(subject) -> MergePolicy:
    values = tuple(
        record.value
        for record in information_of(subject)
        if record.type is CanonicalMergePolicy
    )
    assert len(values) == 1
    return values[0]


def test_default_merge_policy_is_all_without_deprecation_warning() -> None:
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        decorator = canonical_source("Default", filename="default.md", heading="identity")

        @decorator
        class DOCUMENT:
            """Default policy."""

    assert not recorded
    assert _policy(DOCUMENT) is MergePolicy.ALL


def test_deprecated_placeholders_true_maps_to_all() -> None:
    with pytest.warns(DeprecationWarning, match=r'placeholders=True.*merge_policy="all"'):
        decorator = canonical_source(
            "Legacy all",
            filename="legacy-all.md",
            placeholders=True,
            heading="identity",
        )

        @decorator
        class DOCUMENT:
            """Legacy policy."""

    assert _policy(DOCUMENT) is MergePolicy.ALL


def test_deprecated_placeholders_false_maps_to_local() -> None:
    with pytest.warns(DeprecationWarning, match=r'placeholders=False.*merge_policy="local"'):
        decorator = canonical_source(
            "Legacy local",
            filename="legacy-local.md",
            placeholders=False,
            heading="identity",
        )

        @decorator
        class DOCUMENT:
            """Legacy policy."""

    assert _policy(DOCUMENT) is MergePolicy.LOCAL


def test_placeholders_and_merge_policy_cannot_be_combined() -> None:
    with pytest.raises(TypeError, match="both placeholders=.*merge_policy"):
        canonical_source(
            "Conflict",
            filename="conflict.md",
            placeholders=False,
            merge_policy="forbidden",
            heading="identity",
        )


def test_merge_policy_rejects_explicit_none() -> None:
    with pytest.raises(ValueError, match="canonical merge_policy"):
        canonical_source(
            "Invalid",
            filename="invalid.md",
            merge_policy=None,
            heading="identity",
        )


def test_merge_policy_rejects_unknown_keyword() -> None:
    with pytest.raises(ValueError, match="canonical merge_policy"):
        canonical_source(
            "Invalid",
            filename="invalid.md",
            merge_policy="snapshot",
            heading="identity",
        )


def test_all_policy_allows_local_and_external_merge() -> None:
    from tests.fixtures import merge_policy_all

    result = system.validate(merge_policy_all, placement=())
    assert result.is_valid, result.diagnostics
    realizer = MarkdownRealizer(CONTEXT)
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    assert realizer.realize(result.view)[0].content == "# Example\n\nLocal 1.2.3\n"


def test_local_policy_allows_local_but_forbids_external_merge() -> None:
    from tests.fixtures import merge_policy_local

    result = system.validate(merge_policy_local, placement=())
    assert result.is_valid, result.diagnostics
    check = MarkdownRealizer(CONTEXT).check(result.view)
    assert not check.is_realizable
    assert "markdown.document.placeholder.forbidden" in {d.code for d in check.diagnostics}


def test_external_policy_allows_external_merge() -> None:
    from tests.fixtures import merge_policy_external

    result = system.validate(merge_policy_external, placement=())
    assert result.is_valid, result.diagnostics
    realizer = MarkdownRealizer(CONTEXT)
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    assert "Version 1.2.3." in realizer.realize(result.view)[0].content


def test_external_policy_rejects_unused_merge_declaration() -> None:
    from tests.fixtures import merge_policy_external_merge

    result = system.validate(merge_policy_external_merge, placement=())
    assert not result.is_valid
    assert "document.merge.policy.local" in {d.code for d in result.diagnostics}


def test_external_policy_rejects_local_field_reference() -> None:
    from tests.fixtures import merge_policy_external_field

    result = system.validate(merge_policy_external_field, placement=())
    assert not result.is_valid
    assert "document.merge.policy.local" in {d.code for d in result.diagnostics}


def test_forbidden_policy_allows_literal_fields_without_template_merge() -> None:
    from tests.fixtures import merge_policy_forbidden

    result = system.validate(merge_policy_forbidden, placement=())
    assert result.is_valid, result.diagnostics
    realizer = MarkdownRealizer(CONTEXT)
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics
    rendered = realizer.realize(result.view)[0].content
    assert "Historical snapshot." in rendered
    assert "version: 1.2.3" in rendered
    assert "note: Literal {{PROJECT.version}}" in rendered


def test_forbidden_policy_rejects_explicit_merge_declaration() -> None:
    from tests.fixtures import merge_policy_forbidden_merge

    result = system.validate(merge_policy_forbidden_merge, placement=())
    assert not result.is_valid
    assert "document.merge.policy.local" in {d.code for d in result.diagnostics}


def test_forbidden_policy_rejects_external_merge() -> None:
    from tests.fixtures import merge_policy_forbidden_external

    result = system.validate(merge_policy_forbidden_external, placement=())
    assert result.is_valid, result.diagnostics
    check = MarkdownRealizer(CONTEXT).check(result.view)
    assert not check.is_realizable
    assert "markdown.document.placeholder.forbidden" in {d.code for d in check.diagnostics}


def test_cli_surfaces_deprecated_placeholders_warning(tmp_path) -> None:
    env = os.environ.copy()
    root = Path(__file__).resolve().parents[1]
    env["PYTHONPATH"] = os.pathsep.join(
        [str(root / "src"), str(root), env.get("PYTHONPATH", "")]
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "shikumi_devdoc.cli",
            "render",
            "document",
            "tests.fixtures.cli_deprecated_placeholders",
            "-o",
            str(tmp_path),
        ],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert "placeholders=False" in completed.stderr
    assert "deprecated" in completed.stderr
    assert 'merge_policy="local"' in completed.stderr
