"""Lexical rules shared by devdoc placeholder consumers.

The placeholder language is intentionally tiny. ``{{KEY}}`` is semantic syntax,
while ``\\{{...}}`` emits literal double braces and ``${{...}}`` is reserved as
literal host-language syntax (notably GitHub Actions expressions). Keys beginning
with ``#`` are reserved for document section references.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Placeholder:
    """One semantic placeholder occurrence in source text."""

    key: str
    start: int
    end: int


def placeholders(text: str) -> Iterator[Placeholder]:
    """Yield semantic placeholders, excluding escaped and ``${{...}}`` forms."""

    cursor = 0
    while True:
        start = text.find("{{", cursor)
        if start < 0:
            return

        end_marker = text.find("}}", start + 2)
        if end_marker < 0:
            return
        end = end_marker + 2

        # ``\\{{...}}`` is the explicit literal escape. ``${{...}}`` is kept
        # literal so common developer-documentation examples do not collide
        # with devdoc's placeholder language.
        if start > 0 and text[start - 1] in {"\\", "$"}:
            cursor = end
            continue

        key = text[start + 2 : end_marker]
        # Match the previous regex behavior: nested braces are not semantic
        # placeholders. Empty keys were already impossible with ``+``.
        if key and "{" not in key and "}" not in key:
            yield Placeholder(key=key, start=start, end=end)

        cursor = end


def placeholder_keys(text: str) -> tuple[str, ...]:
    """Return semantic placeholder keys in source order."""

    return tuple(placeholder.key for placeholder in placeholders(text))


def expand_placeholders(text: str, resolve: Callable[[str], str]) -> str:
    """Resolve semantic placeholders and remove explicit literal escapes.

    ``\\{{name}}`` becomes ``{{name}}`` without invoking *resolve*. ``${{name}}``
    remains unchanged.
    """

    output: list[str] = []
    cursor = 0

    while True:
        start = text.find("{{", cursor)
        if start < 0:
            output.append(text[cursor:])
            break

        end_marker = text.find("}}", start + 2)
        if end_marker < 0:
            output.append(text[cursor:])
            break
        end = end_marker + 2

        if start > 0 and text[start - 1] == "\\":
            # Include everything before the escape marker, then the literal
            # braces without the escaping backslash.
            output.append(text[cursor : start - 1])
            output.append(text[start:end])
            cursor = end
            continue

        output.append(text[cursor:start])

        if start > 0 and text[start - 1] == "$":
            # The '$' is already present in the preceding slice.
            output.append(text[start:end])
            cursor = end
            continue

        key = text[start + 2 : end_marker]
        if key and "{" not in key and "}" not in key:
            output.append(resolve(key))
        else:
            output.append(text[start:end])
        cursor = end

    return "".join(output)


def section_reference_key(key: str) -> str | None:
    """Return the anchor name when *key* denotes a section reference."""

    if not key.startswith("#") or len(key) == 1:
        return None
    return key[1:]


def section_reference_keys(text: str) -> tuple[str, ...]:
    """Return referenced document anchors in source order, without duplicates."""

    references: list[str] = []
    for key in placeholder_keys(text):
        reference = section_reference_key(key)
        if reference is not None and reference not in references:
            references.append(reference)
    return tuple(references)
