"""Markdown realization for hierarchical developer documents."""

from __future__ import annotations

from collections.abc import Mapping
import re
from types import ModuleType

from shikumi import (
    Diagnostic,
    DiagnosticSeverity,
    RealizationCheck,
    Realizer,
    SemanticView,
    ViewItem,
)

from shikumi_devdoc._placeholder_syntax import placeholder_keys, section_reference_key
from shikumi_devdoc.context import Context, UnknownContextKeyError
from shikumi_devdoc.norms.document import Anchor, Content, Title
from ._header_comment import markdown_header_comment
from ._placeholders import PlaceholderResolver, vocabulary_aliases

_ATX_HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+|$)")
_FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def _markdown_link_label(text: str) -> str:
    """Escape characters that would break a Markdown link label."""

    return text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def _raw_heading_lines(text: str):
    """Yield body-relative line numbers containing semantic-looking raw headings."""

    fence_char: str | None = None
    fence_length = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        if fence_char is not None:
            stripped = line.lstrip(" ")
            indent = len(line) - len(stripped)
            if indent <= 3 and stripped.startswith(fence_char * fence_length):
                run = len(stripped) - len(stripped.lstrip(fence_char))
                if run >= fence_length and not stripped[run:].strip():
                    fence_char = None
                    fence_length = 0
            continue

        fence = _FENCE_OPEN.match(line)
        if fence is not None:
            marker = fence.group(1)
            fence_char = marker[0]
            fence_length = len(marker)
            continue

        if _ATX_HEADING.match(line):
            yield line_number


def _heading_depth(view: SemanticView, item: ViewItem) -> int:
    entities = {entity.subject: entity for entity in view.entities}
    depth = 1
    parent = item.node.parent
    while parent in entities and entities[parent].has(Title):
        depth += 1
        parent = entities[parent].node.parent
    return depth


class MarkdownRealizer(Realizer[str]):
    """Render a document semantic view as Markdown with strict placeholders."""

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
    ) -> "MarkdownRealizer":
        return cls(Context.from_json(text), header_comment=header_comment)

    @staticmethod
    def _anchors(view: SemanticView) -> dict[str, ViewItem]:
        anchors: dict[str, ViewItem] = {}
        for item in view.entities:
            values = item.values(Anchor)
            if len(values) == 1 and values[0] not in anchors:
                anchors[values[0]] = item
        return anchors

    @staticmethod
    def _unknown_non_section_placeholders(
        text: str, resolver: PlaceholderResolver
    ) -> tuple[str, ...]:
        missing: list[str] = []
        for key in placeholder_keys(text):
            if section_reference_key(key) is not None:
                continue
            try:
                resolver.resolve(key)
            except UnknownContextKeyError:
                if key not in missing:
                    missing.append(key)
        return tuple(missing)

    def check(self, view: SemanticView) -> RealizationCheck:
        diagnostics: list[Diagnostic] = []
        roots = self._roots(view)
        if not roots:
            diagnostics.append(
                Diagnostic(
                    "Markdown realization requires at least one top-level heading",
                    code="markdown.document.heading.required",
                )
            )
            return RealizationCheck(view, tuple(diagnostics))

        aliases, alias_diagnostics = vocabulary_aliases(
            roots, code_prefix="markdown.document"
        )
        diagnostics.extend(alias_diagnostics)
        resolver = PlaceholderResolver(self.context, aliases=aliases)
        anchors = self._anchors(view)

        for item in view.entities:
            titles = item.values(Title)
            bodies = item.values(Content)
            if len(titles) != 1:
                diagnostics.append(
                    Diagnostic(
                        "Markdown realization requires exactly one title per heading",
                        code="markdown.document.title.required",
                        subject=item.subject,
                    )
                )
                continue
            if len(bodies) != 1:
                diagnostics.append(
                    Diagnostic(
                        "Markdown realization requires exactly one body per heading",
                        code="markdown.document.content.required",
                        subject=item.subject,
                    )
                )
                continue

            depth = _heading_depth(view, item)
            if depth > 6:
                diagnostics.append(
                    Diagnostic(
                        f"Markdown headings support at most six levels; this heading is at level {depth}",
                        code="markdown.document.heading.depth",
                        subject=item.subject,
                    )
                )

            for line_number in _raw_heading_lines(bodies[0]):
                diagnostics.append(
                    Diagnostic(
                        f"content body contains a raw Markdown heading on body line {line_number}; use a nested TITLE_N entity for document structure",
                        code="markdown.document.heading.raw",
                        severity=DiagnosticSeverity.WARNING,
                        subject=item.subject,
                    )
                )

            for key in placeholder_keys(titles[0]):
                reference = section_reference_key(key)
                if reference is not None:
                    diagnostics.append(
                        Diagnostic(
                            "section-reference placeholders are only supported in document bodies",
                            code="markdown.document.reference.title",
                            subject=item.subject,
                        )
                    )

            for key in placeholder_keys(bodies[0]):
                reference = section_reference_key(key)
                if reference is not None and reference not in anchors:
                    diagnostics.append(
                        Diagnostic(
                            f"document references unknown section anchor {reference!r}",
                            code="markdown.document.reference.unknown",
                            subject=item.subject,
                        )
                    )

            for text in (titles[0], bodies[0]):
                for key in self._unknown_non_section_placeholders(text, resolver):
                    diagnostics.append(
                        Diagnostic(
                            f"document references unknown placeholder {key!r}",
                            code="markdown.document.placeholder.unknown",
                            subject=item.subject,
                        )
                    )

        return RealizationCheck(view, tuple(diagnostics))

    def realize(self, view: SemanticView) -> str:
        roots = self._roots(view)
        vocabulary, _ = vocabulary_aliases(
            roots, code_prefix="markdown.document"
        )
        base_resolver = PlaceholderResolver(self.context, aliases=vocabulary)

        section_aliases: dict[str, str] = {}
        for anchor_name, item in self._anchors(view).items():
            titles = item.values(Title)
            if len(titles) != 1:
                continue
            target_title = base_resolver.expand(titles[0])
            section_aliases[f"#{anchor_name}"] = (
                f"[{_markdown_link_label(target_title)}](#{anchor_name})"
            )

        resolver = PlaceholderResolver(
            self.context,
            aliases={**vocabulary, **section_aliases},
        )
        lines: list[str] = markdown_header_comment(self.header_comment)
        for root in roots:
            self._render_heading(view, root, resolver, depth=1, lines=lines)
        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def _roots(view: SemanticView) -> list[ViewItem]:
        return [
            item
            for item in view.entities
            if isinstance(item.node.parent, ModuleType) and item.has(Title)
        ]

    def _render_heading(
        self,
        view: SemanticView,
        item: ViewItem,
        resolver: PlaceholderResolver,
        *,
        depth: int,
        lines: list[str],
    ) -> None:
        title = resolver.expand(item.values(Title)[0])
        body = resolver.expand(item.values(Content)[0])
        anchors = item.values(Anchor)
        if len(anchors) == 1:
            lines.extend([f'<a id="{anchors[0]}"></a>', ""])
        lines.extend([f"{'#' * depth} {title}", ""])
        if body:
            lines.extend([body, ""])
        for child in view.entities:
            if child.node.parent is item.subject:
                self._render_heading(view, child, resolver, depth=depth + 1, lines=lines)


markdown = MarkdownRealizer()
