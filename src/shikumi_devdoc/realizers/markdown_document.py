"""Small value object for one realized Markdown file."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MarkdownDocument:
    """One Markdown file produced by a realizer."""

    filename: str
    content: str
