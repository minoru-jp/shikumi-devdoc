"""Markdown realization for glossary description bodies."""

from __future__ import annotations

from collections.abc import Mapping

from shikumi import Diagnostic, RealizationCheck, Realizer, SemanticView

from shikumi_devdoc.context import Context
from shikumi_devdoc.norms.vocabulary import Alias, Definition, Deprecated, Glossary, Introduction, Replacement, TermName, Title
from ._header_comment import markdown_header_comment
from ._placeholders import PlaceholderResolver


class MarkdownRealizer(Realizer[str]):
    """Render a glossary semantic view as Markdown."""

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

    def check(self, view: SemanticView) -> RealizationCheck:
        diagnostics: list[Diagnostic] = []
        documents = [item for item in view.entities if item.has(Title)]
        if len(documents) != 1:
            diagnostics.append(Diagnostic("Markdown glossary realization requires exactly one titled document", code="markdown.glossary.document.required"))
            return RealizationCheck(view, tuple(diagnostics))

        document = documents[0]
        if len(document.values(Title)) != 1:
            diagnostics.append(Diagnostic("Markdown glossary realization requires exactly one title", code="markdown.glossary.title.required", subject=document.subject))
        if len(document.values(Introduction)) != 1:
            diagnostics.append(Diagnostic("Markdown glossary realization requires exactly one introduction", code="markdown.glossary.introduction.required", subject=document.subject))

        entries = [item for item in view.entities if item.node.parent is document.subject and item.values(Glossary) == (True,)]
        if not entries:
            diagnostics.append(Diagnostic("Markdown glossary realization requires at least one term", code="markdown.glossary.entries.required", subject=document.subject))

        resolver = PlaceholderResolver(self.context)
        for item, info_types in [(document, (Title, Introduction)), *[(entry, (TermName, Definition)) for entry in entries]]:
            for info_type in info_types:
                values = item.values(info_type)
                if len(values) != 1:
                    diagnostics.append(Diagnostic("Markdown glossary realization requires exactly one value", code="markdown.glossary.value.required", subject=item.subject))
                    continue
                for key in resolver.unknown(values[0]):
                    diagnostics.append(Diagnostic(f"glossary references unknown placeholder {key!r}", code="markdown.glossary.placeholder.unknown", subject=item.subject))

        return RealizationCheck(view, tuple(diagnostics))

    def realize(self, view: SemanticView) -> str:
        resolver = PlaceholderResolver(self.context)
        document = next(item for item in view.entities if item.has(Title))
        title = resolver.expand(document.values(Title)[0])
        introduction = resolver.expand(document.values(Introduction)[0])
        lines = markdown_header_comment(self.header_comment)
        lines.extend([f"# {title}", "", introduction, ""])
        entries = [item for item in view.entities if item.node.parent is document.subject and item.values(Glossary) == (True,)]
        for entry in entries:
            term_name = resolver.expand(entry.values(TermName)[0])
            definition = resolver.expand(entry.values(Definition)[0])
            lines.extend([f"## {term_name}", "", definition, ""])

            aliases = entry.values(Alias)
            if aliases:
                lines.extend([f"**Aliases:** {', '.join(aliases)}", ""])

            if entry.values(Deprecated) == (True,):
                replacements = entry.values(Replacement)
                if replacements:
                    replacement_name = resolver.expand(replacements[0])
                    lines.extend([f"> **Deprecated.** Use {replacement_name} instead.", ""])
                else:
                    lines.extend(["> **Deprecated.**", ""])
        return "\n".join(lines).rstrip() + "\n"


markdown = MarkdownRealizer()
