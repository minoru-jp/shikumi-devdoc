"""Reusable regulation for hierarchical developer-facing documents."""

from __future__ import annotations

from inspect import cleandoc
import re
from types import ModuleType
from typing import TypeVar

from shikumi import (
    Cardinality,
    DescriptorUseRule,
    Diagnostic,
    InformationType,
    Shikumi,
    StructuralKind,
    StructureSelector,
    attach_information,
    record_descriptor_use,
    validator,
)
from shikumi.standard import (
    PackageTreeStructure,
    assignment,
    content_type,
    information_type_rule,
)

from shikumi_devdoc._placeholder_syntax import (
    placeholder_keys,
    section_reference_key,
    section_reference_keys,
)


Title = content_type("title")
Content = content_type("content")
Anchor = InformationType("anchor", str)
SectionReference = InformationType(
    "section reference", str, cardinality=Cardinality.MANY
)


from .common import (
    CanonicalSource,
    VocabularyReference,
    VocabularySource,
    canonical,
    vocabulary,
    vocabulary_reference_diagnostics,
    vocabulary_refs,
)


S = TypeVar("S")
_TITLE_CLASS_NAME = re.compile(r"TITLE_[0-9]+\Z")
_ANCHOR_NAME = re.compile(r"[A-Za-z][A-Za-z0-9._-]*\Z")


class TitleWriter:
    """Describe one document heading using its title and class docstring."""

    __slots__ = ()

    def __call__(self, value: str):
        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            attach_information(subject, Title, value)

            raw = getattr(subject, "__doc__", None)
            if isinstance(raw, str):
                content = cleandoc(raw)
                if not content.strip():
                    content = ""
                attach_information(subject, Content, content)
                for reference in section_reference_keys(content):
                    attach_information(subject, SectionReference, reference)
            return subject

        return apply


title = TitleWriter()
anchor = assignment(Anchor)


def _validate_document_container(view):
    """Validate a document module/package containing top-level titled headings."""

    roots = [
        item
        for item in view.entities
        if isinstance(item.node.parent, ModuleType) and item.has(Title)
    ]
    if not roots:
        yield Diagnostic(
            "document descriptions require at least one top-level heading",
            code="document.heading.required",
        )
        return

    sources = [root for root in roots if len(root.values(CanonicalSource)) == 1]
    if len(sources) != 1:
        yield Diagnostic(
            "document descriptions require exactly one top-level canonical source",
            code="document.canonical_source.required",
        )

    anchored: dict[str, object] = {}
    for item in view.entities:
        values = item.values(Anchor)
        if len(values) != 1:
            continue
        value = values[0]
        previous = anchored.get(value)
        if previous is not None:
            yield Diagnostic(
                f"document anchor {value!r} is already used by another heading",
                code="document.anchor.duplicate",
                subject=item.subject,
            )
        else:
            anchored[value] = item.subject

    for item in view.entities:
        for reference in item.values(SectionReference):
            if reference not in anchored:
                yield Diagnostic(
                    f"document references unknown section anchor {reference!r}",
                    code="document.section_reference.unknown",
                    subject=item.subject,
                )


@validator(focus=StructuralKind.MODULE)
def document_module(view):
    """Validate a standalone document module."""

    yield from _validate_document_container(view)


@validator(focus=StructuralKind.PACKAGE)
def document_package(view):
    """Validate a document package."""

    yield from _validate_document_container(view)


@validator(focus=StructuralKind.ENTITY)
def document_entity(view):
    """Validate heading entities in a document description body."""

    item = view.focused
    if len(item.values(Title)) != 1:
        yield Diagnostic(
            "document heading entities require exactly one title",
            code="document.title.required",
        )
    if len(item.values(Content)) != 1:
        yield Diagnostic(
            "document heading entities require exactly one content body",
            code="document.content.required",
        )

    for title_text in item.values(Title):
        if any(
            section_reference_key(marker) is not None
            for marker in placeholder_keys(title_text)
        ):
            yield Diagnostic(
                "section-reference placeholders are only supported in document bodies",
                code="document.section_reference.title",
            )

    anchors = item.values(Anchor)
    if len(anchors) == 1 and _ANCHOR_NAME.fullmatch(anchors[0]) is None:
        yield Diagnostic(
            "document anchors must start with an ASCII letter and contain only ASCII letters, digits, '.', '_' or '-'",
            code="document.anchor.syntax",
        )

    subject_name = getattr(item.subject, "__name__", "")
    if _TITLE_CLASS_NAME.fullmatch(subject_name) is None:
        yield Diagnostic(
            "document heading class names must match TITLE_<decimal digits>",
            code="document.heading.name",
        )

    is_top_level = isinstance(item.node.parent, ModuleType)
    sources = item.values(CanonicalSource)
    if not is_top_level and sources:
        yield Diagnostic(
            "canonical source belongs on a top-level heading",
            code="document.canonical_source.top_level_only",
        )
    if len(sources) > 1:
        yield Diagnostic(
            "document headings allow at most one canonical source",
            code="document.canonical_source.cardinality",
        )

    yield from vocabulary_reference_diagnostics(
        item,
        (*item.values(Title), *item.values(Content)),
        code_prefix="document",
    )

    vocabularies = item.values(VocabularySource)
    if not is_top_level and vocabularies:
        yield Diagnostic(
            "document vocabulary belongs on top-level headings",
            code="document.vocabulary.top_level_only",
        )
    if len(vocabularies) > 1:
        yield Diagnostic(
            "document headings allow at most one vocabulary",
            code="document.vocabulary.cardinality",
        )

    for child in view.entities:
        if child.node.parent is item.subject and len(child.values(Title)) != 1:
            yield Diagnostic(
                "document heading children must also be titled headings",
                code="document.heading.child",
                subject=child.subject,
            )


_entity = StructureSelector(kind=StructuralKind.ENTITY)

document = Shikumi(
    structure=PackageTreeStructure(),
    information_types=[
        Title,
        Content,
        Anchor,
        SectionReference,
        CanonicalSource,
        VocabularySource,
        VocabularyReference,
    ],
    descriptor_rules=[
        DescriptorUseRule(descriptor=title, allowed=_entity, name="title"),
        DescriptorUseRule(descriptor=anchor, allowed=_entity, name="anchor"),
        DescriptorUseRule(descriptor=canonical, allowed=_entity, name="canonical"),
        DescriptorUseRule(descriptor=vocabulary, allowed=_entity, name="vocabulary"),
        DescriptorUseRule(
            descriptor=vocabulary_refs, allowed=_entity, name="vocabulary_refs"
        ),
    ],
    validators=[
        information_type_rule(Title),
        information_type_rule(Content),
        information_type_rule(Anchor),
        information_type_rule(SectionReference),
        information_type_rule(CanonicalSource),
        information_type_rule(VocabularySource),
        information_type_rule(VocabularyReference),
        document_module,
        document_package,
        document_entity,
    ],
)
