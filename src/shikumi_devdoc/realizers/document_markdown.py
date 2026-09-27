"""Markdown realization for generic canonical developer documents."""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Mapping
from enum import Enum
from inspect import cleandoc
import posixpath
import sys
from urllib.parse import quote

from shikumi import (
    Diagnostic,
    DiagnosticSeverity,
    RealizationCheck,
    Realizer,
    SemanticView,
    ViewItem,
    information_of,
)

from shikumi_devdoc._placeholder_syntax import expand_placeholders, placeholder_keys
from shikumi_devdoc.context import Context, UnknownContextKeyError
from shikumi_devdoc.norms._common import (
    APPEND,
    CanonicalContent,
    CanonicalDocumentPath,
    CanonicalFilename,
    CanonicalHeadingPolicy,
    CanonicalPlaceholders,
    CanonicalSource,
    CanonicalTitle,
    CanonicalUnreferencedFields,
    HeadingPolicy,
    MergeBinding,
)
from shikumi_devdoc.norms._document import (
    DocumentField,
    FieldPresentation,
    FieldValue,
    Title,
    document_node_identity,
    _FieldReference,
    _field_values_for_reference,
    template_reference_bindings,
)
from shikumi_devdoc.norms._vocabulary import vocabulary_term_name
from ._document_collection import canonical_documents, ordered_canonical_documents
from ._header_comment import markdown_header_comment
from ._markdown_heading import heading_depth, heading_fragment, raw_heading_lines
from ._placeholders import PlaceholderResolver
from .markdown_document import MarkdownDocument


class MarkdownRealizer(Realizer[tuple[MarkdownDocument, ...]]):
    """Render canonical document nodes and fields without domain-specific semantics."""

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

    @staticmethod
    def _children(view: SemanticView, subject: object) -> list[ViewItem]:
        return [item for item in view.entities if item.node.parent is subject]

    def _resolver(self) -> PlaceholderResolver:
        return PlaceholderResolver(self.context)

    def _header_for(self, item: ViewItem) -> str | None:
        if self.header_comment is None:
            return None
        sources = item.values(CanonicalSource)
        if len(sources) == 1:
            return self.header_comment.replace("{canonical_source}", sources[0])
        return self.header_comment

    def _document_members(self, view: SemanticView, document: ViewItem) -> list[ViewItem]:
        members = [document]

        def visit(subject: object) -> None:
            for child in self._children(view, subject):
                members.append(child)
                visit(child.subject)

        visit(document.subject)
        return members

    @staticmethod
    def _group_fields(item: ViewItem) -> list[tuple[str, list[FieldValue]]]:
        grouped: OrderedDict[str, list[FieldValue]] = OrderedDict()
        for field_value in item.values(DocumentField):
            if isinstance(field_value, FieldValue):
                grouped.setdefault(field_value.binding_name, []).append(field_value)
        return list(grouped.items())

    @staticmethod
    def _reference_bindings(item: ViewItem) -> dict[str, object]:
        return template_reference_bindings(item)[0]

    @staticmethod
    def _ambiguous_reference_names(item: ViewItem) -> set[str]:
        return set(template_reference_bindings(item)[1])

    def _external_keys(self, item: ViewItem, text: str) -> tuple[str, ...]:
        local = self._reference_bindings(item)
        ambiguous = self._ambiguous_reference_names(item)
        return tuple(
            key
            for key in placeholder_keys(text)
            if key not in local and key not in ambiguous
        )

    def _referenced_field_bindings(self, item: ViewItem, text: str) -> set[str]:
        bindings = self._reference_bindings(item)
        result: set[str] = set()
        for key in placeholder_keys(text):
            target = bindings.get(key)
            if isinstance(target, _FieldReference):
                result.add(target.binding_name)
        return result

    @staticmethod
    def _python_identity(value: type[object]) -> str:
        semantic = document_node_identity(value)
        if semantic is not None:
            return semantic
        module = getattr(value, "__module__", "")
        qualname = getattr(value, "__qualname__", getattr(value, "__name__", ""))
        if module and qualname:
            return f"{module}.{qualname}"
        return qualname or repr(value)

    @staticmethod
    def _information_values(subject: object, information_type) -> tuple[object, ...]:
        return tuple(
            record.value
            for record in information_of(subject)
            if record.type is information_type
        )

    @classmethod
    def _canonical_root_for(cls, subject: type[object]) -> type[object] | None:
        module_name = getattr(subject, "__module__", "")
        qualname = getattr(subject, "__qualname__", "")
        if not module_name or not qualname or "<locals>" in qualname:
            return None
        module = sys.modules.get(module_name)
        if module is None:
            return None
        current: object = module
        root: type[object] | None = None
        for part in qualname.split("."):
            current = getattr(current, part, None)
            if current is None:
                return None
            if isinstance(current, type):
                titles = cls._information_values(current, CanonicalTitle)
                if len(titles) == 1:
                    root = current
        return root

    @classmethod
    def _reference_metadata(
        cls,
        target: object,
        resolver: PlaceholderResolver,
    ) -> tuple[type[object], str, str, str | None] | None:
        if not isinstance(target, type):
            return None
        root = cls._canonical_root_for(target)
        if root is None:
            return None
        paths = cls._information_values(root, CanonicalDocumentPath)
        if len(paths) != 1 or not isinstance(paths[0], str):
            return None
        document_path = paths[0]

        if target is root:
            titles = cls._information_values(root, CanonicalTitle)
            if len(titles) != 1 or not isinstance(titles[0], str):
                return None
            return root, document_path, resolver.expand(titles[0]), None

        if document_node_identity(target) is None:
            return None
        policies = cls._information_values(root, CanonicalHeadingPolicy)
        if len(policies) != 1 or policies[0] is not HeadingPolicy.IDENTITY:
            return None
        heading = target.__name__
        fragment = heading_fragment(heading)
        if not fragment:
            return None
        return root, document_path, heading, fragment

    @staticmethod
    def _escape_link_label(value: str) -> str:
        return value.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")

    def _render_reference_value(
        self,
        value: object,
        resolver: PlaceholderResolver,
        *,
        source_document: object,
    ) -> str:
        if isinstance(value, (tuple, list)):
            return ", ".join(
                self._render_reference_value(
                    item,
                    resolver,
                    source_document=source_document,
                )
                for item in value
            )
        if isinstance(value, set):
            return ", ".join(
                sorted(
                    self._render_reference_value(
                        item,
                        resolver,
                        source_document=source_document,
                    )
                    for item in value
                )
            )

        metadata = self._reference_metadata(value, resolver)
        if metadata is None:
            if isinstance(value, type):
                return f"`{self._python_identity(value)}`"
            return self._render_literal_value(value)

        target_root, target_path, label, anchor = metadata
        source_paths = self._information_values(source_document, CanonicalDocumentPath)
        if len(source_paths) != 1 or not isinstance(source_paths[0], str):
            if isinstance(value, type):
                return f"`{self._python_identity(value)}`"
            return self._render_literal_value(value)
        source_path = source_paths[0]

        if target_root is source_document and anchor is not None:
            href = f"#{quote(anchor, safe='._-~')}"
        else:
            source_directory = posixpath.dirname(source_path) or "."
            relative_path = posixpath.relpath(target_path, start=source_directory)
            encoded_path = quote(relative_path, safe="/._-~")
            if anchor is None:
                href = encoded_path
            else:
                href = f"{encoded_path}#{quote(anchor, safe='._-~')}"
        return f"[{self._escape_link_label(label)}]({href})"

    def _render_literal_value(self, value: object) -> str:
        """Render literal field data without placeholder interpretation."""

        if isinstance(value, str):
            return value
        if isinstance(value, type):
            return f"`{self._python_identity(value)}`"
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, (tuple, list)):
            return ", ".join(self._render_literal_value(item) for item in value)
        if isinstance(value, set):
            return ", ".join(sorted(self._render_literal_value(item) for item in value))
        if value is None:
            return "None"
        return str(value)

    @staticmethod
    def _render_list_item(value: str) -> list[str]:
        rows = value.splitlines() or [""]
        rendered = [f"- {rows[0]}"]
        rendered.extend(f"  {row}" if row else "" for row in rows[1:])
        return rendered


    @staticmethod
    def _table_cell(value: str) -> str:
        return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")

    def _render_reference_target(
        self,
        item: ViewItem,
        name: str,
        target: object,
        resolver: PlaceholderResolver,
        *,
        stack: tuple[str, ...],
        source_filename: str,
        source_document: object,
    ) -> str:
        if isinstance(target, str):
            return target

        values = _field_values_for_reference(item, target)
        if values:
            return self._render_field_content(
                item,
                values,
                resolver,
                stack=(*stack, name),
                source_filename=source_filename,
                source_document=source_document,
            )

        term_name = vocabulary_term_name(target)
        if term_name is not None:
            return term_name

        return "{{" + name + "}}"

    def _render_template(
        self,
        item: ViewItem,
        text: str,
        resolver: PlaceholderResolver,
        *,
        stack: tuple[str, ...] = (),
        source_filename: str,
        source_document: object,
    ) -> str:
        bindings = self._reference_bindings(item)
        ambiguous = self._ambiguous_reference_names(item)

        def resolve(key: str) -> str:
            if key in ambiguous:
                return "{{" + key + "}}"
            if key not in bindings:
                return resolver.resolve(key)
            if key in stack:
                return "{{" + key + "}}"
            return self._render_reference_target(
                item,
                key,
                bindings[key],
                resolver,
                stack=stack,
                source_filename=source_filename,
                source_document=source_document,
            )

        return expand_placeholders(text, resolve)

    def _render_field_content(
        self,
        item: ViewItem,
        values: list[FieldValue],
        resolver: PlaceholderResolver,
        *,
        stack: tuple[str, ...],
        source_filename: str,
        source_document: object,
    ) -> str:
        if not values:
            return ""
        presentation = values[0].presentation

        if presentation is FieldPresentation.INLINE:
            rendered = [self._render_literal_value(entry.value) for entry in values]
            if len(rendered) == 1:
                return rendered[0]
            if all("\n" not in value for value in rendered):
                return ", ".join(rendered)
            return "\n\n".join(rendered)

        if presentation is FieldPresentation.REFERENCE:
            rendered = [
                self._render_reference_value(
                    entry.value,
                    resolver,
                    source_document=source_document,
                )
                for entry in values
            ]
            if len(rendered) == 1:
                return rendered[0]
            if all("\n" not in value for value in rendered):
                return ", ".join(rendered)
            return "\n\n".join(rendered)

        if presentation is FieldPresentation.LIST:
            lines: list[str] = []
            for entry in values:
                lines.extend(self._render_list_item(self._render_literal_value(entry.value)))
            return "\n".join(lines)

        if presentation is FieldPresentation.TEST_TARGET:
            rendered = [cleandoc(self._render_literal_value(entry.value)) for entry in values]
            return "\n\n".join(rendered)

        if presentation is FieldPresentation.TABLE:
            columns = values[0].columns
            lines = [
                "| " + " | ".join(self._table_cell(column) for column in columns) + " |",
                "| " + " | ".join("---" for _ in columns) + " |",
            ]
            for entry in values:
                row = entry.value
                if not isinstance(row, (tuple, list)):
                    continue
                cells = [
                    self._table_cell(self._render_literal_value(cell))
                    for cell in row
                ]
                lines.append("| " + " | ".join(cells) + " |")
            return "\n".join(lines)

        if presentation is FieldPresentation.PROSE:
            rendered: list[str] = []
            for entry in values:
                if isinstance(entry.value, str):
                    rendered.append(
                        self._render_template(
                            item,
                            entry.value,
                            resolver,
                            stack=stack,
                            source_filename=source_filename,
                            source_document=source_document,
                        )
                    )
            return "\n\n".join(rendered)

        raise ValueError(f"unknown document field presentation: {presentation!r}")

    def _append_field_block(
        self,
        item: ViewItem,
        values: list[FieldValue],
        resolver: PlaceholderResolver,
        lines: list[str],
        *,
        source_filename: str,
        source_document: object,
    ) -> None:
        if not values:
            return
        name = values[0].schema.name
        content = self._render_field_content(
            item,
            values,
            resolver,
            stack=(),
            source_filename=source_filename,
            source_document=source_document,
        )
        presentation = values[0].presentation

        if presentation in {FieldPresentation.INLINE, FieldPresentation.REFERENCE} and "\n" not in content:
            lines.extend([f"{name}: {content}", ""])
            return

        lines.extend([f"{name}:", ""])
        if content:
            lines.extend([content, ""])

    def _append_candidates(self, item: ViewItem) -> list[tuple[str, list[FieldValue]]]:
        grouped = self._group_fields(item)
        suppressed: set[str] = set()

        for body in item.values(CanonicalContent):
            if isinstance(body, str):
                suppressed.update(self._referenced_field_bindings(item, body))

        for _, values in grouped:
            for entry in values:
                if entry.presentation is FieldPresentation.PROSE and isinstance(entry.value, str):
                    suppressed.update(self._referenced_field_bindings(item, entry.value))

        return [(name, values) for name, values in grouped if name not in suppressed]

    def check(self, view: SemanticView) -> RealizationCheck:
        diagnostics: list[Diagnostic] = []
        documents = canonical_documents(view)
        if not documents:
            diagnostics.append(
                Diagnostic(
                    "Markdown realization requires at least one canonical document",
                    code="markdown.document.required",
                )
            )
            return RealizationCheck(view, tuple(diagnostics))

        resolver = self._resolver()

        for document in documents:
            placeholders_allowed = document.values(CanonicalPlaceholders) == (True,)
            for item in self._document_members(view, document):
                depth = heading_depth(view, item, (CanonicalContent,))
                if depth > 6:
                    diagnostics.append(
                        Diagnostic(
                            f"Markdown headings support at most six levels; this heading is at level {depth}",
                            code="markdown.document.heading.depth",
                            subject=item.subject,
                        )
                    )

                for body in item.values(CanonicalContent):
                    if not isinstance(body, str):
                        continue
                    for line_number in raw_heading_lines(body):
                        diagnostics.append(
                            Diagnostic(
                                f"content template contains a raw Markdown heading on body line {line_number}; use a nested class for document structure",
                                code="markdown.document.heading.raw",
                                severity=DiagnosticSeverity.WARNING,
                                subject=item.subject,
                            )
                        )

                for field_value in item.values(DocumentField):
                    if (
                        isinstance(field_value, FieldValue)
                        and field_value.presentation is FieldPresentation.PROSE
                        and isinstance(field_value.value, str)
                    ):
                        for line_number in raw_heading_lines(field_value.value):
                            diagnostics.append(
                                Diagnostic(
                                    f"prose field {field_value.binding_name!r} contains a raw Markdown heading on line {line_number}; use a nested class for document structure",
                                    code="markdown.document.heading.raw",
                                    severity=DiagnosticSeverity.WARNING,
                                    subject=item.subject,
                                )
                            )

                template_texts = [
                    value
                    for value in item.values(CanonicalContent)
                    if isinstance(value, str)
                ]
                template_texts.extend(
                    field_value.value
                    for field_value in item.values(DocumentField)
                    if isinstance(field_value, FieldValue)
                    and field_value.presentation is FieldPresentation.PROSE
                    and isinstance(field_value.value, str)
                )
                title_texts = [
                    value
                    for info_type in (CanonicalTitle, Title)
                    for value in item.values(info_type)
                    if isinstance(value, str)
                ]

                for text in (*title_texts, *template_texts):
                    ambiguous = self._ambiguous_reference_names(item)
                    for key in placeholder_keys(text):
                        if key in ambiguous:
                            diagnostics.append(
                                Diagnostic(
                                    f"local template reference {key!r} is ambiguous",
                                    code="markdown.document.reference.ambiguous",
                                    subject=item.subject,
                                )
                            )
                    for key in self._external_keys(item, text):
                        if not placeholders_allowed:
                            diagnostics.append(
                                Diagnostic(
                                    f"canonical document forbids external placeholder {key!r}",
                                    code="markdown.document.placeholder.forbidden",
                                    subject=item.subject,
                                )
                            )
                            continue
                        try:
                            resolver.resolve(key)
                        except UnknownContextKeyError:
                            diagnostics.append(
                                Diagnostic(
                                    f"canonical document references unknown external placeholder {key!r}",
                                    code="markdown.document.placeholder.unknown",
                                    subject=item.subject,
                                )
                            )

                titles = item.values(Title)
                if len(titles) == 1 and isinstance(titles[0], str):
                    try:
                        rendered_title = self._render_template(
                            item,
                            titles[0],
                            resolver,
                            source_filename=document.values(CanonicalFilename)[0],
                            source_document=document.subject,
                        )
                    except UnknownContextKeyError:
                        rendered_title = None
                    if rendered_title is not None and (
                        not rendered_title.strip()
                        or "\n" in rendered_title
                        or "\r" in rendered_title
                    ):
                        diagnostics.append(
                            Diagnostic(
                                "document node title must realize to one non-empty line",
                                code="markdown.document.title.value",
                                subject=item.subject,
                            )
                        )

        return RealizationCheck(view, tuple(diagnostics))

    def _node_title(
        self,
        item: ViewItem,
        resolver: PlaceholderResolver,
        *,
        heading_policy: HeadingPolicy,
        source_filename: str,
        source_document: object,
    ) -> str:
        if heading_policy is HeadingPolicy.IDENTITY:
            return item.node.name
        titles = item.values(Title)
        if len(titles) != 1 or not isinstance(titles[0], str):
            return item.node.name
        return self._render_template(
            item,
            titles[0],
            resolver,
            source_filename=source_filename,
            source_document=source_document,
        )

    def _render_node(
        self,
        view: SemanticView,
        item: ViewItem,
        resolver: PlaceholderResolver,
        *,
        depth: int,
        field_policy,
        heading_policy: HeadingPolicy,
        lines: list[str],
        source_filename: str,
        source_document: object,
    ) -> None:
        lines.extend([
            f"{'#' * depth} "
            f"{self._node_title(item, resolver, heading_policy=heading_policy, source_filename=source_filename, source_document=source_document)}",
            "",
        ])
        bodies = item.values(CanonicalContent)
        body = bodies[0] if len(bodies) == 1 else ""
        if body:
            rendered = self._render_template(
                item,
                body,
                resolver,
                source_filename=source_filename,
                source_document=source_document,
            )
            if rendered:
                lines.extend([rendered, ""])

        if heading_policy is HeadingPolicy.IDENTITY:
            titles = item.values(Title)
            if len(titles) == 1 and isinstance(titles[0], str):
                rendered_title = self._render_template(
                    item,
                    titles[0],
                    resolver,
                    source_filename=source_filename,
                    source_document=source_document,
                )
                lines.extend([f"title: {rendered_title}", ""])

        if field_policy is APPEND:
            for _, values in self._append_candidates(item):
                self._append_field_block(
                    item,
                    values,
                    resolver,
                    lines,
                    source_filename=source_filename,
                    source_document=source_document,
                )

        for child in self._children(view, item.subject):
            self._render_node(
                view,
                child,
                resolver,
                depth=depth + 1,
                field_policy=field_policy,
                heading_policy=heading_policy,
                lines=lines,
                source_filename=source_filename,
                source_document=source_document,
            )

    def _render_document(
        self,
        view: SemanticView,
        document: ViewItem,
        resolver: PlaceholderResolver,
    ) -> MarkdownDocument:
        lines = markdown_header_comment(self._header_for(document))
        source_filename = document.values(CanonicalFilename)[0]
        title = resolver.expand(document.values(CanonicalTitle)[0])
        field_policy = document.values(CanonicalUnreferencedFields)[0]
        heading_policy = document.values(CanonicalHeadingPolicy)[0]
        lines.extend([f"# {title}", ""])

        body = document.values(CanonicalContent)[0]
        if body:
            rendered = self._render_template(
                document,
                body,
                resolver,
                source_filename=source_filename,
                source_document=document.subject,
            )
            if rendered:
                lines.extend([rendered, ""])

        if field_policy is APPEND:
            for _, values in self._append_candidates(document):
                self._append_field_block(
                    document,
                    values,
                    resolver,
                    lines,
                    source_filename=source_filename,
                    source_document=document.subject,
                )

        for child in self._children(view, document.subject):
            self._render_node(
                view,
                child,
                resolver,
                depth=2,
                field_policy=field_policy,
                heading_policy=heading_policy,
                lines=lines,
                source_filename=source_filename,
                source_document=document.subject,
            )

        return MarkdownDocument(
            source_filename,
            "\n".join(lines).rstrip() + "\n",
        )

    def realize(self, view: SemanticView) -> tuple[MarkdownDocument, ...]:
        resolver = self._resolver()
        return tuple(
            self._render_document(view, document, resolver)
            for document in ordered_canonical_documents(view)
        )


markdown = MarkdownRealizer()
