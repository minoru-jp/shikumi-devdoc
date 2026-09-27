"""Lexical rules shared by devdoc placeholder consumers.

The placeholder language is intentionally tiny. ``{{name}}`` denotes a semantic
placeholder. A canonical document node may satisfy it from its local template
namespace: field bindings participate automatically under their ``@=`` left-hand
name, while ``merge`` can add class targets, literals, or explicit aliases. Class
targets use the shortest unambiguous suffix of their Python identity. A local
name collision is an error only when an ambiguous reference is used. Otherwise
document realizers may resolve the placeholder from external context when that
canonical source allows external placeholders. ``\\{{...}}`` emits literal double
braces and ``${{...}}`` is reserved as literal host-language syntax, notably
GitHub Actions expressions.
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

        if start > 0 and text[start - 1] in {"\\", "$"}:
            cursor = end
            continue

        key = text[start + 2 : end_marker]
        if key and "{" not in key and "}" not in key:
            yield Placeholder(key=key, start=start, end=end)

        cursor = end


def placeholder_keys(text: str) -> tuple[str, ...]:
    """Return semantic placeholder keys in source order."""

    return tuple(placeholder.key for placeholder in placeholders(text))


def expand_placeholders(text: str, resolve: Callable[[str], str]) -> str:
    """Resolve semantic placeholders and remove explicit literal escapes.

    ``\\{{name}}`` becomes ``{{name}}`` without invoking *resolve*.
    ``${{name}}`` remains unchanged.
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
            output.append(text[cursor : start - 1])
            output.append(text[start:end])
            cursor = end
            continue

        output.append(text[cursor:start])

        if start > 0 and text[start - 1] == "$":
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
