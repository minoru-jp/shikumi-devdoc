"""Formatting helpers for optional Markdown header comments."""

from __future__ import annotations


def markdown_header_comment(text: str | None) -> list[str]:
    """Render caller-provided text as a Markdown HTML comment block."""

    if text is None or not text.strip():
        return []
    if "-->" in text:
        raise ValueError("Markdown header comments must not contain '-->'")
    return ["<!--", *text.strip().splitlines(), "-->", ""]
