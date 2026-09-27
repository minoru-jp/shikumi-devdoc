"""Shared external-context placeholder resolution for Markdown realizers."""

from __future__ import annotations

from collections.abc import Mapping

from shikumi_devdoc._placeholder_syntax import expand_placeholders, placeholder_keys
from shikumi_devdoc.context import Context, UnknownContextKeyError, normalize_context


class PlaceholderResolver:
    """Resolve dotted external-context paths.

    Local canonical-document merges are resolved by the document realizer before
    falling back to this external resolver.
    """

    __slots__ = ("context",)

    def __init__(self, context: Context | Mapping | None = None) -> None:
        self.context = normalize_context(context)

    def resolve(self, key: str) -> str:
        return self.context.resolve(key)

    def unknown(self, text: str) -> tuple[str, ...]:
        missing: list[str] = []
        for key in placeholder_keys(text):
            try:
                self.resolve(key)
            except UnknownContextKeyError:
                if key not in missing:
                    missing.append(key)
        return tuple(missing)

    def expand(self, text: str) -> str:
        return expand_placeholders(text, self.resolve)
