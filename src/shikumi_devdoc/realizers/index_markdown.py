"""Markdown index realization for canonical-document packages."""

from __future__ import annotations

from collections.abc import Mapping
from urllib.parse import quote

from shikumi import Diagnostic, RealizationCheck, Realizer, SemanticView, StructuralKind

from shikumi_devdoc._placeholder_syntax import placeholder_keys
from shikumi_devdoc.context import Context, UnknownContextKeyError
from shikumi_devdoc.norms._common import (
    CanonicalFilename,
    CanonicalPlaceholders,
    CanonicalSummary,
    CanonicalTitle,
)
from shikumi_devdoc.norms._document import template_reference_bindings
from shikumi_devdoc.norms._partitioned import validate_filename
from ._document_collection import canonical_documents, ordered_canonical_documents
from ._header_comment import markdown_header_comment
from ._placeholders import PlaceholderResolver
from .markdown_document import MarkdownDocument


class IndexMarkdownRealizer(Realizer[MarkdownDocument]):
    """Render one collection index from a package-level canonical-document view."""

    def __init__(
        self,
        context: Context | Mapping | None = None,
        *,
        title: str = "Index",
        filename: str = "INDEX.md",
        header_comment: str | None = None,
    ) -> None:
        if not isinstance(title, str):
            raise TypeError("index title must be a string")
        if not title.strip():
            raise ValueError("index title must be non-empty")
        self.context = context
        self.title = title
        self.filename = validate_filename(filename, label="index filename")
        self.header_comment = header_comment

    def _resolver(self) -> PlaceholderResolver:
        return PlaceholderResolver(self.context)

    @staticmethod
    def _local_reference_names(document) -> set[str]:
        bindings, ambiguous = template_reference_bindings(document)
        return set(bindings) | set(ambiguous)

    @staticmethod
    def _table_cell(value: str) -> str:
        return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")

    @staticmethod
    def _link_target(filename: str) -> str:
        return quote(filename, safe="/._-~")

    def check(self, view: SemanticView) -> RealizationCheck:
        diagnostics: list[Diagnostic] = []

        if view.focused.kind is not StructuralKind.PACKAGE:
            diagnostics.append(
                Diagnostic(
                    "Markdown index realization requires a package focus",
                    code="markdown.index.package.required",
                    subject=view.focus.subject,
                )
            )
            return RealizationCheck(view, tuple(diagnostics))

        documents = canonical_documents(view)
        if not documents:
            diagnostics.append(
                Diagnostic(
                    "Markdown index realization requires at least one canonical document in the package",
                    code="markdown.index.document.required",
                    subject=view.focus.subject,
                )
            )
            return RealizationCheck(view, tuple(diagnostics))

        resolver = self._resolver()

        for key in placeholder_keys(self.title):
            try:
                resolver.resolve(key)
            except UnknownContextKeyError:
                diagnostics.append(
                    Diagnostic(
                        f"index title references unknown external placeholder {key!r}",
                        code="markdown.index.placeholder.unknown",
                        subject=view.focus.subject,
                    )
                )

        for document in documents:
            filenames = document.values(CanonicalFilename)
            if len(filenames) == 1 and filenames[0].casefold() == self.filename.casefold():
                diagnostics.append(
                    Diagnostic(
                        f"index filename {self.filename!r} collides with a canonical document output",
                        code="markdown.index.filename.collision",
                        subject=document.subject,
                    )
                )

            titles = document.values(CanonicalTitle)
            summaries = document.values(CanonicalSummary)
            if len(summaries) != 1:
                diagnostics.append(
                    Diagnostic(
                        "Markdown index realization requires exactly one @summary(...) on each canonical document",
                        code="markdown.index.summary.required",
                        subject=document.subject,
                    )
                )

            local = self._local_reference_names(document)
            placeholders_allowed = document.values(CanonicalPlaceholders) == (True,)
            for label, texts in (("title", titles), ("summary", summaries)):
                if len(texts) != 1:
                    continue
                text = texts[0]
                for key in placeholder_keys(text):
                    if key in local:
                        diagnostics.append(
                            Diagnostic(
                                f"canonical document {label} cannot use local template reference {key!r}",
                                code=(
                                    "markdown.index.summary.reference"
                                    if label == "summary"
                                    else "markdown.index.title.reference"
                                ),
                                subject=document.subject,
                            )
                        )
                        continue
                    if not placeholders_allowed:
                        diagnostics.append(
                            Diagnostic(
                                f"canonical document forbids external placeholder {key!r} in its {label}",
                                code="markdown.index.placeholder.forbidden",
                                subject=document.subject,
                            )
                        )
                        continue
                    try:
                        resolver.resolve(key)
                    except UnknownContextKeyError:
                        diagnostics.append(
                            Diagnostic(
                                f"canonical document {label} references unknown external placeholder {key!r}",
                                code="markdown.index.placeholder.unknown",
                                subject=document.subject,
                            )
                        )

        return RealizationCheck(view, tuple(diagnostics))

    def realize(self, view: SemanticView) -> MarkdownDocument:
        resolver = self._resolver()
        lines = markdown_header_comment(self.header_comment)
        lines.extend([f"# {resolver.expand(self.title)}", ""])
        lines.extend(["| Document | Summary |", "| --- | --- |"])

        for document in ordered_canonical_documents(view):
            title = resolver.expand(document.values(CanonicalTitle)[0])
            summary = resolver.expand(document.values(CanonicalSummary)[0])
            filename = document.values(CanonicalFilename)[0]
            link = f"[{self._table_cell(title)}]({self._link_target(filename)})"
            lines.append(f"| {link} | {self._table_cell(summary)} |")

        return MarkdownDocument(self.filename, "\n".join(lines).rstrip() + "\n")


markdown = IndexMarkdownRealizer()
