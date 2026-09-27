"""Reusable regulation for project vocabulary and glossary sources."""

from __future__ import annotations

from inspect import cleandoc
import re
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

from .common import CanonicalSource, canonical


Title = content_type("title")
Introduction = content_type("introduction")
TermName = InformationType("term", str)
Definition = content_type("definition")
PreserveSpelling = InformationType("preserve spelling", bool)
Glossary = InformationType("glossary", bool)
Alias = InformationType("alias", str, Cardinality.MANY)
Deprecated = InformationType("deprecated", bool)
Replacement = InformationType("replacement", str)


S = TypeVar("S")
_TERM_CLASS_NAME = re.compile(r"TERM_[0-9]+\Z")


class TitleWriter:
    """Describe the glossary artifact title and introduction on a vocabulary root."""

    __slots__ = ()

    def __call__(self, value: str):
        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            attach_information(subject, Title, value)

            raw = getattr(subject, "__doc__", None)
            if isinstance(raw, str):
                attach_information(subject, Introduction, cleandoc(raw))
            return subject

        return apply


class TermWriter:
    """Describe one vocabulary entry using its name and the class docstring."""

    __slots__ = ()

    def __call__(self, name: str):
        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            attach_information(subject, TermName, name)

            raw = getattr(subject, "__doc__", None)
            if isinstance(raw, str):
                attach_information(subject, Definition, cleandoc(raw))
            return subject

        return apply


title = TitleWriter()
term = TermWriter()
preserve_spelling = assignment(PreserveSpelling)
glossary = assignment(Glossary)
alias = assignment(Alias)
deprecated = assignment(Deprecated)
replacement = assignment(Replacement)


def _validate_vocabulary_container(view):
    """Validate a vocabulary module/package containing one vocabulary root."""

    roots = [
        item
        for item in view.entities
        if item.node.parent is view.focused.subject and item.has(Title)
    ]
    if len(roots) != 1:
        yield Diagnostic(
            "vocabulary descriptions require exactly one titled top-level root",
            code="vocabulary.document.required",
        )
        return

    if len(roots[0].values(CanonicalSource)) != 1:
        yield Diagnostic(
            "vocabulary root requires exactly one canonical source",
            code="vocabulary.canonical_source.required",
            subject=roots[0].subject,
        )


def _validate_vocabulary_relationships(view):
    roots = [item for item in view.entities if item.has(Title)]
    if len(roots) != 1:
        return

    root = roots[0]
    entries = [item for item in view.entities if item.node.parent is root.subject]
    term_by_subject = {item.subject: item for item in entries if len(item.values(TermName)) == 1}

    canonical_names: dict[str, object] = {}
    for item in term_by_subject.values():
        name = item.values(TermName)[0]
        previous = canonical_names.get(name)
        if previous is not None and previous is not item.subject:
            yield Diagnostic(
                f"term name {name!r} is used by more than one vocabulary entry",
                code="vocabulary.term.duplicate",
                subject=item.subject,
            )
        else:
            canonical_names[name] = item.subject

    claimed_names = dict(canonical_names)
    for item in term_by_subject.values():
        seen_here: set[str] = set()
        for value in item.values(Alias):
            if not value.strip():
                yield Diagnostic(
                    "vocabulary aliases must not be empty",
                    code="vocabulary.alias.empty",
                    subject=item.subject,
                )
                continue
            if value in seen_here:
                yield Diagnostic(
                    f"vocabulary alias {value!r} is repeated on the same term",
                    code="vocabulary.alias.duplicate",
                    subject=item.subject,
                )
                continue
            seen_here.add(value)
            previous = claimed_names.get(value)
            if previous is not None and previous is not item.subject:
                yield Diagnostic(
                    f"vocabulary alias {value!r} conflicts with another term or alias",
                    code="vocabulary.alias.conflict",
                    subject=item.subject,
                )
            elif value in canonical_names and canonical_names[value] is item.subject:
                yield Diagnostic(
                    f"vocabulary alias {value!r} duplicates its canonical term name",
                    code="vocabulary.alias.canonical",
                    subject=item.subject,
                )
            else:
                claimed_names[value] = item.subject

        replacements = item.values(Replacement)
        if replacements:
            if item.values(Deprecated) != (True,):
                yield Diagnostic(
                    "replacement requires deprecated @= True",
                    code="vocabulary.replacement.requires_deprecated",
                    subject=item.subject,
                )
            target_name = replacements[0]
            own_name = item.values(TermName)[0]
            if target_name == own_name:
                yield Diagnostic(
                    "deprecated terms cannot replace themselves",
                    code="vocabulary.replacement.self",
                    subject=item.subject,
                )
            elif target_name not in canonical_names:
                yield Diagnostic(
                    f"replacement {target_name!r} must name another canonical term in the same vocabulary",
                    code="vocabulary.replacement.target",
                    subject=item.subject,
                )


@validator(focus=StructuralKind.MODULE)
def vocabulary_module(view):
    """Validate a standalone vocabulary module."""

    yield from _validate_vocabulary_container(view)
    yield from _validate_vocabulary_relationships(view)


@validator(focus=StructuralKind.PACKAGE)
def vocabulary_package(view):
    """Validate a vocabulary package."""

    yield from _validate_vocabulary_container(view)
    yield from _validate_vocabulary_relationships(view)


@validator(focus=StructuralKind.ENTITY)
def vocabulary_entity(view):
    """Validate the vocabulary root and vocabulary entry entities."""

    entry = view.focused
    titles = entry.values(Title)
    terms = entry.values(TermName)

    if titles:
        if len(titles) != 1:
            yield Diagnostic(
                "vocabulary root requires exactly one glossary title",
                code="vocabulary.title.required",
            )
        if len(entry.values(Introduction)) != 1:
            yield Diagnostic(
                "vocabulary root requires exactly one glossary introduction",
                code="vocabulary.introduction.required",
            )
        if entry.node.name != "VOCABULARY":
            yield Diagnostic(
                "vocabulary root entity must be named VOCABULARY",
                code="vocabulary.document.name",
            )
        if len(entry.values(CanonicalSource)) != 1:
            yield Diagnostic(
                "vocabulary root requires exactly one canonical source",
                code="vocabulary.canonical_source.required",
            )
        if any(
            entry.values(info_type)
            for info_type in (Alias, Deprecated, Replacement, PreserveSpelling, Glossary)
        ):
            yield Diagnostic(
                "term metadata belongs on vocabulary entries, not the vocabulary root",
                code="vocabulary.term_metadata.entry_only",
            )

        direct_children = [
            item for item in view.entities if item.node.parent is entry.subject
        ]
        if not direct_children:
            yield Diagnostic(
                "vocabulary root requires at least one term entry",
                code="vocabulary.entries.required",
            )
        for child in direct_children:
            if len(child.values(TermName)) != 1:
                yield Diagnostic(
                    "vocabulary root children must be term entries",
                    code="vocabulary.entries.child",
                    subject=child.subject,
                )
        return

    if terms:
        if entry.values(CanonicalSource):
            yield Diagnostic(
                "canonical source belongs on the vocabulary root",
                code="vocabulary.canonical_source.root_only",
            )
        subject_name = getattr(entry.subject, "__name__", "")
        if _TERM_CLASS_NAME.fullmatch(subject_name) is None:
            yield Diagnostic(
                "vocabulary entry class names must match TERM_<decimal digits>",
                code="vocabulary.entry.name",
            )

        if len(terms) != 1:
            yield Diagnostic(
                "vocabulary entries require exactly one term name",
                code="vocabulary.term.required",
            )

        if len(entry.values(Definition)) != 1:
            yield Diagnostic(
                "vocabulary entries require exactly one definition",
                code="vocabulary.definition.required",
            )
        for value in entry.values(Deprecated):
            if value is False:
                yield Diagnostic(
                    "omit deprecated metadata instead of writing deprecated @= False",
                    code="vocabulary.deprecated.false",
                    subject=entry.subject,
                )
        return

    yield Diagnostic(
        "vocabulary entities must be the vocabulary root or a term entry",
        code="vocabulary.entity.kind",
    )


_entity = StructureSelector(kind=StructuralKind.ENTITY)

vocabulary_system = Shikumi(
    structure=PackageTreeStructure(),
    information_types=[
        Title,
        Introduction,
        TermName,
        Definition,
        PreserveSpelling,
        Glossary,
        Alias,
        Deprecated,
        Replacement,
        CanonicalSource,
    ],
    descriptor_rules=[
        DescriptorUseRule(descriptor=title, allowed=_entity, name="title"),
        DescriptorUseRule(descriptor=canonical, allowed=_entity, name="canonical"),
        DescriptorUseRule(descriptor=term, allowed=_entity, name="term"),
        DescriptorUseRule(
            descriptor=preserve_spelling,
            allowed=_entity,
            name="preserve_spelling",
        ),
        DescriptorUseRule(descriptor=glossary, allowed=_entity, name="glossary"),
        DescriptorUseRule(descriptor=alias, allowed=_entity, name="alias"),
        DescriptorUseRule(descriptor=deprecated, allowed=_entity, name="deprecated"),
        DescriptorUseRule(descriptor=replacement, allowed=_entity, name="replacement"),
    ],
    validators=[
        information_type_rule(Title),
        information_type_rule(Introduction),
        information_type_rule(TermName),
        information_type_rule(Definition),
        information_type_rule(PreserveSpelling),
        information_type_rule(Glossary),
        information_type_rule(Alias),
        information_type_rule(Deprecated),
        information_type_rule(Replacement),
        information_type_rule(CanonicalSource),
        vocabulary_module,
        vocabulary_package,
        vocabulary_entity,
    ],
)
