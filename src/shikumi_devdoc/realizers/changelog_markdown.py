"""Markdown realization for structured project changelogs."""

from __future__ import annotations

from collections.abc import Mapping
from types import ModuleType

from shikumi import Diagnostic, RealizationCheck, Realizer, SemanticView, ViewItem

from shikumi_devdoc.context import Context
from shikumi_devdoc.norms.changelog import Breaking, ChangeContent, ChangeKind, ChangeKindInformation, ChangelogTitle, Introduction, ReleaseDate, ReleaseLabel, ReleaseNotes, Unreleased, _ordered_releases
from ._header_comment import markdown_header_comment
from ._placeholders import PlaceholderResolver, vocabulary_aliases


class ChangelogMarkdownRealizer(Realizer[str]):
    """Render a changelog semantic view as Markdown grouped by category."""

    def __init__(
        self,
        context: Context | Mapping | None = None,
        *,
        header_comment: str | None = None,
    ) -> None:
        self.context = context
        self.header_comment = header_comment

    @classmethod
    def from_json(
        cls,
        text: str,
        *,
        header_comment: str | None = None,
    ) -> "ChangelogMarkdownRealizer":
        return cls(Context.from_json(text), header_comment=header_comment)

    def check(self, view: SemanticView) -> RealizationCheck:
        diagnostics: list[Diagnostic] = []
        roots = self._roots(view)
        if len(roots) != 1:
            diagnostics.append(Diagnostic("changelog Markdown realization requires exactly one root", code="markdown.changelog.root.required"))
            return RealizationCheck(view, tuple(diagnostics))

        aliases, alias_diagnostics = vocabulary_aliases(roots, code_prefix="markdown.changelog")
        diagnostics.extend(alias_diagnostics)
        resolver = PlaceholderResolver(self.context, aliases=aliases)
        for item in view.entities:
            values: tuple[str, ...] = (*item.values(ChangelogTitle), *item.values(Introduction), *item.values(ReleaseLabel), *item.values(ReleaseNotes), *item.values(ChangeContent))
            for text in values:
                for key in resolver.unknown(text):
                    diagnostics.append(Diagnostic(f"changelog references unknown placeholder {key!r}", code="markdown.changelog.placeholder.unknown", subject=item.subject))

        expanded_labels: dict[str, object] = {}
        for release in _ordered_releases(view, roots[0]):
            if release.values(Unreleased) == (True,):
                continue
            labels = release.values(ReleaseLabel)
            if len(labels) != 1 or resolver.unknown(labels[0]):
                continue
            label = resolver.expand(labels[0])
            if label in expanded_labels:
                diagnostics.append(
                    Diagnostic(
                        f"rendered release label {label!r} is already used",
                        code="markdown.changelog.release.label.duplicate",
                        subject=release.subject,
                    )
                )
            else:
                expanded_labels[label] = release.subject
        return RealizationCheck(view, tuple(diagnostics))

    def realize(self, view: SemanticView) -> str:
        root = self._roots(view)[0]
        aliases, _ = vocabulary_aliases([root], code_prefix="markdown.changelog")
        resolver = PlaceholderResolver(self.context, aliases=aliases)
        title = resolver.expand(root.values(ChangelogTitle)[0])
        introduction = resolver.expand(root.values(Introduction)[0])
        lines = markdown_header_comment(self.header_comment)
        lines.extend([f"# {title}", ""])
        if introduction:
            lines.extend([introduction, ""])

        for release in _ordered_releases(view, root):
            if release.values(Unreleased) == (True,):
                label = "Unreleased"
            else:
                label = resolver.expand(release.values(ReleaseLabel)[0])
            dates = release.values(ReleaseDate)
            heading = f"## {label}" + (f" - {dates[0]}" if dates else "")
            lines.extend([heading, ""])
            notes = resolver.expand(release.values(ReleaseNotes)[0])
            if notes:
                lines.extend([notes, ""])

            grouped: dict[ChangeKind, list[ViewItem]] = {}
            order: list[ChangeKind] = []
            for item in self._children(view, release):
                kind = item.values(ChangeKindInformation)[0]
                if kind not in grouped:
                    grouped[kind] = []
                    order.append(kind)
                grouped[kind].append(item)

            for kind in order:
                lines.extend([f"### {kind.value}", ""])
                for item in grouped[kind]:
                    content = resolver.expand(item.values(ChangeContent)[0])
                    lines.extend(self._bullet(content, breaking=item.values(Breaking) == (True,)))
                lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def _roots(view: SemanticView) -> list[ViewItem]:
        return [item for item in view.entities if isinstance(item.node.parent, ModuleType) and item.has(ChangelogTitle)]

    @staticmethod
    def _children(view: SemanticView, parent: ViewItem) -> list[ViewItem]:
        return [item for item in view.entities if item.node.parent is parent.subject]

    @staticmethod
    def _bullet(content: str, *, breaking: bool = False) -> list[str]:
        rows = content.splitlines() or [""]
        prefix = "**Breaking:** " if breaking else ""
        rendered = [f"- {prefix}{rows[0]}"]
        rendered.extend(f"  {row}" if row else "" for row in rows[1:])
        return rendered


markdown = ChangelogMarkdownRealizer()
