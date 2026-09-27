"""Shared Markdown heading checks for semantic document realizers."""

from __future__ import annotations

import re

from shikumi import InformationType, SemanticView, ViewItem

_ATX_HEADING = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+|$)")
_FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def raw_heading_lines(text: str):
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


def heading_fragment(text: str) -> str:
    """Return the logical Markdown fragment derived from one rendered heading.

    The transformation intentionally mirrors the common heading-slug convention
    used by GitHub-style Markdown renderers: lowercase the heading, remove
    punctuation other than ``-`` and ``_``, and replace whitespace with ``-``.
    The result is a logical publication fragment, not a guarantee about any
    particular downstream Markdown renderer.
    """

    lowered = text.strip().lower()
    kept = "".join(
        character
        for character in lowered
        if character.isalnum() or character in {"-", "_"} or character.isspace()
    )
    return re.sub(r"\s+", "-", kept)


def heading_depth(
    view: SemanticView,
    item: ViewItem,
    heading_types: tuple[InformationType, ...],
) -> int:
    """Return the Markdown depth implied by nested semantic headings."""

    entities = {entity.subject: entity for entity in view.entities}
    depth = 1
    parent = item.node.parent
    while parent in entities and any(entities[parent].has(kind) for kind in heading_types):
        depth += 1
        parent = entities[parent].node.parent
    return depth
