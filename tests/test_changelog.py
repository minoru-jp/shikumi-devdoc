from tests.fixtures import changelog_reference_mismatch, changelog_source
from shikumi_devdoc.norms.changelog import changelog_system
from shikumi_devdoc.realizers.changelog_markdown import ChangelogMarkdownRealizer


def test_changelog_renders_vocabulary_and_external_context() -> None:
    result = changelog_system.validate(changelog_source, placement=())
    assert result.is_valid, result.diagnostics

    realizer = ChangelogMarkdownRealizer(
        {"PROJECT": {"name": "Example", "version": "0.1.0"}},
        header_comment="運用側の注意書き\n\n運用側の公開方針",
    )
    check = realizer.check(result.view)
    assert check.is_realizable, check.diagnostics

    rendered = realizer.realize(result.view)
    assert rendered == (
        "<!--\n"
        "運用側の注意書き\n\n"
        "運用側の公開方針\n"
        "-->\n\n"
        "# Example Changelog\n\n"
        "Release history for Example.\n\n"
        "## 0.1.0 - 2026-09-13\n\n"
        "First public release.\n\n"
        "### Added\n\n"
        "- Added Widget support.\n"
    )


def test_changelog_vocabulary_references_are_local_to_each_entity() -> None:
    result = changelog_system.validate(changelog_reference_mismatch, placement=())
    assert not result.is_valid

    diagnostics = {(diagnostic.code, diagnostic.subject) for diagnostic in result.diagnostics}
    assert (
        "changelog.vocabulary_reference.missing",
        changelog_reference_mismatch.CHANGELOG.RELEASE_1.CHANGE_1,
    ) in diagnostics


def test_changelog_unreleased_and_breaking_semantics_render() -> None:
    from tests.fixtures import changelog_semantics
    from shikumi_devdoc.norms.changelog import Breaking, Unreleased

    result = changelog_system.validate(changelog_semantics, placement=())
    assert result.is_valid, result.diagnostics

    unreleased_entry = next(item for item in result.view.entities if item.node.name == "RELEASE_1")
    breaking_change = next(
        item
        for item in result.view.entities
        if item.node.name == "CHANGE_1" and item.node.parent is changelog_semantics.CHANGELOG.RELEASE_1
    )
    assert unreleased_entry.values(Unreleased) == (True,)
    assert breaking_change.values(Breaking) == (True,)

    rendered = ChangelogMarkdownRealizer().realize(result.view)
    assert "## Unreleased\n" in rendered
    assert "- **Breaking:** Changed the wire format." in rendered
    assert "## 1.0.0 - 2026-09-13" in rendered


def test_changelog_unreleased_is_unique_first_and_undated() -> None:
    from tests.fixtures import changelog_invalid_semantics

    result = changelog_system.validate(changelog_invalid_semantics, placement=())
    assert not result.is_valid
    codes = {diagnostic.code for diagnostic in result.diagnostics}
    assert "changelog.unreleased.order" in codes
    assert "changelog.unreleased.date" in codes


def test_changelog_package_composes_parts_by_explicit_order() -> None:
    from tests.fixtures import changelog_partitioned
    from shikumi_devdoc.norms.changelog import ChangelogPartOrder

    result = changelog_system.validate(changelog_partitioned, placement=())
    assert result.is_valid, result.diagnostics

    parts = [item for item in result.view.entities if item.has(ChangelogPartOrder)]
    assert sorted(item.values(ChangelogPartOrder)[0] for item in parts) == [10, 20]

    rendered = ChangelogMarkdownRealizer().realize(result.view)
    assert rendered.index("## Unreleased") < rendered.index("## 2.0.0 - 2026-01-01")
    assert rendered.index("## 2.0.0 - 2026-01-01") < rendered.index("## 1.0.0 - 2025-01-01")


def test_changelog_package_validates_global_partition_invariants() -> None:
    from tests.fixtures import changelog_partition_invalid

    result = changelog_system.validate(changelog_partition_invalid, placement=())
    assert not result.is_valid
    codes = {diagnostic.code for diagnostic in result.diagnostics}
    assert "changelog.part.order.duplicate" in codes
    assert "changelog.unreleased.cardinality" in codes
    assert "changelog.release.label.duplicate" in codes
