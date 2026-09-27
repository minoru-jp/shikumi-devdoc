from pathlib import Path

from shikumi_devdoc.cli import main


def test_render_command_accepts_explicit_notice_and_json_context(tmp_path: Path) -> None:
    output = tmp_path / "document"
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
    rendered = (output / "document_source.md").read_text(encoding="utf-8")
    assert rendered.startswith("<!--\nGenerated.\nCanonical: `")
    assert "tests/fixtures/document_source.py" in rendered.split("-->", 1)[0]
    assert "# Example" in rendered


def test_render_command_rejects_invalid_context_json(tmp_path: Path, capsys) -> None:
    output = tmp_path / "invalid-context"
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
    output = tmp_path / "no-notice"
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
    rendered = (output / "plain_document_source.md").read_text(encoding="utf-8")
    assert rendered.startswith("# Plain\n")
    assert "SHOULD NOT APPEAR" not in rendered


def test_cli_formats_diagnostics_with_code_subject_and_source(tmp_path: Path, capsys) -> None:
    output = tmp_path / "diagnostics"
    exit_code = main([
        "render",
        "document",
        "tests.fixtures.document_reference_mismatch",
        "-o",
        str(output),
    ])

    assert exit_code == 1
    error = capsys.readouterr().err
    assert "error [markdown.document.placeholder.forbidden]" in error
    assert "tests/fixtures/document_reference_mismatch.py:" in error
    assert "tests.fixtures.document_reference_mismatch.TITLE_1.TITLE_2" in error
    assert "canonical document forbids external placeholder 'widget'" in error


def test_render_command_can_emit_translation_source_metadata(tmp_path: Path) -> None:
    output = tmp_path / "translation"
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
    rendered = (output / "document_source.md").read_text(encoding="utf-8")
    assert rendered.startswith("<!-- shikumi-devdoc:translation-metadata\n")
    assert '"identifier": "TERM_2"' in rendered
    assert '"text": "InternalName"' in rendered
    assert "\n# Example\n" in rendered


def test_cli_prints_non_fatal_warnings(tmp_path: Path, capsys) -> None:
    output = tmp_path / "warnings-fatal"
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
    output = tmp_path / "warnings"
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
    assert (output / "document_raw_heading.md").exists()


def test_render_document_writes_each_declared_document_to_output_directory(tmp_path: Path) -> None:
    output = tmp_path / "document"
    notice = tmp_path / "notice.toml"
    notice.write_text('[notice]\ncontent = "Canonical: `{canonical_source}`."\n', encoding="utf-8")

    exit_code = main([
        "render",
        "document",
        "tests.fixtures.structured_document_source",
        "-o",
        str(output),
        "--context",
        '{"PROJECT":{"name":"Demo"}}',
        "--notice",
        str(notice),
    ])

    assert exit_code == 0
    assert sorted(path.name for path in output.iterdir()) == ["rendering.md", "validation.md"]

    validation = (output / "validation.md").read_text(encoding="utf-8")
    rendering = (output / "rendering.md").read_text(encoding="utf-8")
    assert "# Validation" in validation
    assert "Validation rules for Demo." in validation
    assert "## SourceValidation" in validation
    assert "### RejectInvalidSource" in validation
    assert "level: MUST" in validation
    assert "## level" not in validation
    assert "tests/fixtures/structured_document_source.py" in validation.split("-->", 1)[0]
    assert "tests/fixtures/structured_document_source.py" in rendering.split("-->", 1)[0]




def test_render_index_collects_package_documents(tmp_path: Path) -> None:
    output = tmp_path / "index"
    exit_code = main([
        "render",
        "index",
        "tests.fixtures.index_source",
        "-o",
        str(output),
        "--context",
        '{"PROJECT":{"name":"Example"}}',
        "--index-title",
        "Example Reference",
    ])

    assert exit_code == 0
    rendered = (output / "INDEX.md").read_text(encoding="utf-8")
    assert rendered.startswith("# Example Reference\n\n")
    assert "[Example Core](core.md)" in rendered
    assert "[Guide](guide.md)" in rendered


def test_render_index_rejects_module_focus(tmp_path: Path, capsys) -> None:
    output = tmp_path / "index-module"
    exit_code = main([
        "render",
        "index",
        "tests.fixtures.index_source.core",
        "-o",
        str(output),
        "--context",
        '{"PROJECT":{"name":"Example"}}',
    ])

    assert exit_code == 1
    assert "markdown.index.package.required" in capsys.readouterr().err
