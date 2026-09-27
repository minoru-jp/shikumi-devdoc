"""Shared placeholder and vocabulary resolution for Markdown realizers."""

from __future__ import annotations

from collections.abc import Mapping
from types import ModuleType

from shikumi import Diagnostic, ViewItem

from shikumi_devdoc._placeholder_syntax import expand_placeholders, placeholder_keys
from shikumi_devdoc.context import Context, UnknownContextKeyError, normalize_context
from shikumi_devdoc.norms.common import VocabularySource
from shikumi_devdoc.norms.vocabulary import TermName, vocabulary_system


class PlaceholderResolver:
    """Resolve vocabulary aliases first, then dotted external context paths."""

    __slots__ = ("context", "aliases")

    def __init__(self, context: Context | Mapping | None = None, *, aliases: Mapping[str, str] | None = None) -> None:
        self.context = normalize_context(context)
        self.aliases = dict(aliases or {})

    def resolve(self, key: str) -> str:
        if key in self.aliases:
            return self.aliases[key]
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


def vocabulary_aliases(items: list[ViewItem] | tuple[ViewItem, ...], *, code_prefix: str) -> tuple[dict[str, str], tuple[Diagnostic, ...]]:
    sources = [
        source
        for item in items
        for source in item.values(VocabularySource)
    ]
    if not sources:
        return {}, ()
    if len(sources) != 1:
        subject = items[0].subject if items else None
        return {}, (
            Diagnostic(
                "Markdown realization allows at most one vocabulary",
                code=f"{code_prefix}.vocabulary.multiple",
                subject=subject,
            ),
        )

    source = sources[0]
    try:
        placement = () if isinstance(source, ModuleType) and not hasattr(source, "__path__") else None
        result = vocabulary_system.validate(source, placement=placement)
    except Exception as exc:
        return {}, (
            Diagnostic(
                f"vocabulary could not be interpreted: {exc}",
                code=f"{code_prefix}.vocabulary.invalid",
            ),
        )

    if not result.is_valid:
        return {}, (
            Diagnostic(
                "vocabulary does not satisfy the vocabulary regulation",
                code=f"{code_prefix}.vocabulary.invalid",
            ),
        )

    aliases = {
        item.node.name: item.values(TermName)[0]
        for item in result.view.entities
        if len(item.values(TermName)) == 1
    }
    return aliases, ()
