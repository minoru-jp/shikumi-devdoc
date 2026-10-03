"""Markdown realization for Vocabulary semantic views."""

from __future__ import annotations

from collections.abc import Mapping

from shikumi import Diagnostic, RealizationCheck, Realizer, SemanticView, ViewItem

from shikumi_devdoc._placeholder_syntax import placeholder_keys
from shikumi_devdoc.context import Context, UnknownContextKeyError
from shikumi_devdoc.norms._common import (
    CanonicalContent,
    CanonicalMergePolicy,
    CanonicalTitle,
    MergePolicy,
)
from shikumi_devdoc.norms._vocabulary import (
    Alias,
    Definition,
    Deprecated,
    Glossary,
    Replacement,
    TermName,
    VocabularyProfile,
)

from ._header_comment import markdown_header_comment
from ._placeholders import PlaceholderResolver


def _is_public_glossary_entry(item: ViewItem) -> bool:
    """Return the effective glossary-selection value for one vocabulary term."""

    values = item.values(Glossary)
    return values in ((), (True,))


class MarkdownRealizer(Realizer[str]):
    """Render a Vocabulary semantic view as Markdown glossary content."""

    context: Context | Mapping[str, object] | None
    header_comment: str | None

    def __init__(
        self,
        context: Context | Mapping[str, object] | None = None,
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
    ) -> MarkdownRealizer:
        return cls(Context.from_json(text), header_comment=header_comment)

    def check(self, view: SemanticView) -> RealizationCheck:
        diagnostics: list[Diagnostic] = []
        documents = [
            item for item in view.entities if item.values(VocabularyProfile) == (True,)
        ]
        if len(documents) != 1:
            diagnostics.append(
                Diagnostic(
                    "Markdown glossary realization requires exactly one @vocabulary root",
                    code="markdown.glossary.document.required",
                )
            )
            return RealizationCheck(view, tuple(diagnostics))

        document = documents[0]
        if len(document.values(CanonicalTitle)) != 1:
            diagnostics.append(
                Diagnostic(
                    "Markdown glossary realization requires exactly one canonical title",
                    code="markdown.glossary.title.required",
                    subject=document.subject,
                )
            )
        if len(document.values(CanonicalContent)) != 1:
            diagnostics.append(
                Diagnostic(
                    "Markdown glossary realization requires exactly one introduction",
                    code="markdown.glossary.introduction.required",
                    subject=document.subject,
                )
            )

        entries = [
            item
            for item in view.entities
            if item.node.parent is document.subject and _is_public_glossary_entry(item)
        ]
        if not entries:
            diagnostics.append(
                Diagnostic(
                    "Markdown glossary realization requires at least one public term",
                    code="markdown.glossary.entries.required",
                    subject=document.subject,
                )
            )

        resolver = PlaceholderResolver(self.context)
        policies = document.values(CanonicalMergePolicy)
        merge_policy = policies[0] if len(policies) == 1 else MergePolicy.ALL
        pairs = [
            (document, (CanonicalTitle, CanonicalContent)),
            *[(entry, (Definition,)) for entry in entries],
        ]
        for item, info_types in pairs:
            for info_type in info_types:
                values = item.values(info_type)
                if len(values) != 1:
                    diagnostics.append(
                        Diagnostic(
                            "Markdown glossary realization requires exactly one value",
                            code="markdown.glossary.value.required",
                            subject=item.subject,
                        )
                    )
                    continue
                for key in placeholder_keys(values[0]):
                    if not merge_policy.allows_external:
                        diagnostics.append(
                            Diagnostic(
                                f"canonical vocabulary forbids external placeholder {key!r}",
                                code="markdown.glossary.placeholder.forbidden",
                                subject=item.subject,
                            )
                        )
                        continue
                    try:
                        _ = resolver.resolve(key)
                    except UnknownContextKeyError:
                        diagnostics.append(
                            Diagnostic(
                                f"glossary references unknown placeholder {key!r}",
                                code="markdown.glossary.placeholder.unknown",
                                subject=item.subject,
                            )
                        )

        return RealizationCheck(view, tuple(diagnostics))

    def realize(self, view: SemanticView) -> str:
        resolver = PlaceholderResolver(self.context)
        document = next(
            item for item in view.entities if item.values(VocabularyProfile) == (True,)
        )
        title = resolver.expand(document.values(CanonicalTitle)[0])
        introduction = resolver.expand(document.values(CanonicalContent)[0])
        lines = markdown_header_comment(self.header_comment)
        lines.extend([f"# {title}", "", introduction, ""])
        entries = [
            item
            for item in view.entities
            if item.node.parent is document.subject and _is_public_glossary_entry(item)
        ]
        for entry in entries:
            term_name = entry.values(TermName)[0]
            definition = resolver.expand(entry.values(Definition)[0])
            lines.extend([f"## {term_name}", "", definition, ""])

            aliases = entry.values(Alias)
            if aliases:
                lines.extend([f"**Aliases:** {', '.join(aliases)}", ""])

            if entry.values(Deprecated) == (True,):
                replacements = entry.values(Replacement)
                if replacements:
                    lines.extend(
                        [f"> **Deprecated.** Use {replacements[0]} instead.", ""]
                    )
                else:
                    lines.extend(["> **Deprecated.**", ""])
        return "\n".join(lines).rstrip() + "\n"


markdown = MarkdownRealizer()
