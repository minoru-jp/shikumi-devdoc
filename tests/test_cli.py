from pathlib import Path

from shikumi_devdoc.cli import main


def test_terms_command_generates_reference_module(tmp_path: Path) -> None:
    output = tmp_path / "terms.py"
    exit_code = main([
        "terms",
        "tests.fixtures.vocabulary_source",
        "-o",
        str(output),
    ])

    assert exit_code == 0
    content = output.read_text(encoding="utf-8")
    assert "class TERM_1:" in content
    assert "Widget" in content


def test_render_command_accepts_explicit_notice_and_json_context(tmp_path: Path) -> None:
    output = tmp_path / "README.md"
    context = '{"PROJECT":{"name":"Example","version":"0.1.0"},"PYTHON":{"minimum":"3.11"}}'
    notice = tmp_path / "notice.toml"
    notice.write_text(
        '[notice]\ncontent = """Generated.\nCanonical: `{canonical_source}`.\n"""\n',
        encoding="utf-8",
    )

    exit_code = main([
        "render",
        "document",
        "tests.fixtures.document_source",
        "-o",
        str(output),
        "--context",
        context,
        "--notice",
        str(notice),
    ])

    assert exit_code == 0
    rendered = output.read_text(encoding="utf-8")
    assert rendered.startswith("<!--\nGenerated.\nCanonical: `")
    assert "tests/fixtures/document_source.py" in rendered.split("-->", 1)[0]
    assert "# Example" in rendered


def test_render_command_rejects_invalid_context_json(tmp_path: Path, capsys) -> None:
    output = tmp_path / "README.md"
    exit_code = main([
        "render",
        "document",
        "tests.fixtures.plain_document_source",
        "-o",
        str(output),
        "--context",
        "{invalid",
    ])

    assert exit_code == 1
    assert "invalid context JSON" in capsys.readouterr().err

def test_render_command_does_not_search_for_notice(tmp_path: Path) -> None:
    output = tmp_path / "README.md"
    context = '{"PROJECT":{"name":"Plain"}}'
    (tmp_path / "notice.toml").write_text(
        '[notice]\ncontent = "SHOULD NOT APPEAR"\n',
        encoding="utf-8",
    )

    exit_code = main([
        "render",
        "document",
        "tests.fixtures.plain_document_source",
        "-o",
        str(output),
        "--context",
        context,
    ])

    assert exit_code == 0
    rendered = output.read_text(encoding="utf-8")
    assert rendered.startswith("# Plain\n")
    assert "SHOULD NOT APPEAR" not in rendered


def test_cli_formats_diagnostics_with_code_subject_and_source(tmp_path: Path, capsys) -> None:
    output = tmp_path / "README.md"
    exit_code = main([
        "render",
        "document",
        "tests.fixtures.document_reference_mismatch",
        "-o",
        str(output),
    ])

    assert exit_code == 1
    error = capsys.readouterr().err
    assert "error [document.vocabulary_reference.unused]" in error
    assert "tests/fixtures/document_reference_mismatch.py:" in error
    assert "tests.fixtures.document_reference_mismatch.TITLE_1" in error
    assert "TERM_1 is listed in vocabulary_refs but not used by this entity" in error


def test_render_command_can_emit_translation_source_metadata(tmp_path: Path) -> None:
    output = tmp_path / "README.md"
    context = '{"PROJECT":{"name":"Example","version":"0.1.0"},"PYTHON":{"minimum":"3.11"}}'

    exit_code = main([
        "render",
        "document",
        "tests.fixtures.document_source",
        "-o",
        str(output),
        "--context",
        context,
        "--translation-source",
    ])

    assert exit_code == 0
    rendered = output.read_text(encoding="utf-8")
    assert rendered.startswith("<!-- shikumi-devdoc:translation-metadata\n")
    assert '"identifier": "TERM_2"' in rendered
    assert '"text": "InternalName"' in rendered
    assert "\n# Example\n" in rendered


def test_cli_prints_non_fatal_warnings(tmp_path: Path, capsys) -> None:
    output = tmp_path / "README.md"
    exit_code = main([
        "render",
        "document",
        "tests.fixtures.document_structural_markdown",
        "-o",
        str(output),
    ])

    # The level-7 heading is still fatal, but the warning must also be visible.
    assert exit_code == 1
    error = capsys.readouterr().err
    assert "warning [markdown.document.heading.raw]" in error
    assert "error [markdown.document.heading.depth]" in error


def test_cli_warning_does_not_prevent_rendering(tmp_path: Path, capsys) -> None:
    output = tmp_path / "README.md"
    exit_code = main([
        "render",
        "document",
        "tests.fixtures.document_raw_heading",
        "-o",
        str(output),
    ])

    assert exit_code == 0
    error = capsys.readouterr().err
    assert "warning [markdown.document.heading.raw]" in error
    assert output.exists()


def test_render_changelog_package_uses_semantic_canonical_source_in_notice(tmp_path: Path) -> None:
    output = tmp_path / "CHANGELOG.md"
    notice = tmp_path / "notice.toml"
    notice.write_text(
        '[notice]\ncontent = "Canonical: `{canonical_source}`."\n',
        encoding="utf-8",
    )

    exit_code = main([
        "render",
        "changelog",
        "tests.fixtures.changelog_partitioned",
        "-o",
        str(output),
        "--notice",
        str(notice),
    ])

    assert exit_code == 0
    rendered = output.read_text(encoding="utf-8")
    header = rendered.split("-->", 1)[0]
    assert "tests/fixtures/changelog_partitioned/canonical.py" in header
    assert "tests/fixtures/changelog_partitioned/__init__.py" not in header
    assert rendered.index("## 2.0.0") < rendered.index("## 1.0.0")
