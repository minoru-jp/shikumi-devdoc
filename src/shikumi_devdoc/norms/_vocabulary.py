"""Vocabulary semantic profile for canonical developer documents."""

from __future__ import annotations

from inspect import cleandoc
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
    information_of,
    record_descriptor_use,
    validator,
)
from shikumi.standard import (
    PackageTreeStructure,
    assignment,
    content_type,
    information_type_rule,
)

from ._common import (
    CanonicalContent,
    CanonicalDocumentPath,
    CanonicalFilename,
    CanonicalHeadingPolicy,
    CanonicalPlaceholders,
    CanonicalSource,
    CanonicalTitle,
    CanonicalUnreferencedFields,
    canonical_source,
)


VocabularyProfile = InformationType("vocabulary profile", bool)
TermName = InformationType("term", str)
Definition = content_type("definition")
PreserveSpelling = InformationType("preserve spelling", bool)
Glossary = InformationType("glossary", bool)
Alias = InformationType("alias", str, Cardinality.MANY)
Deprecated = InformationType("deprecated", bool)
Replacement = InformationType("replacement", str)


def canonical_vocabulary_term(target: object) -> type[object] | None:
    """Return a canonical Vocabulary term class when ``target`` is one.

    Vocabulary terms are referenced directly. A class is a canonical term only
    when the ``@vocabulary`` profile attached exactly one semantic ``TermName``.
    """

    if not isinstance(target, type):
        return None
    names = [
        record.value
        for record in information_of(target)
        if record.type is TermName
    ]
    if len(names) != 1:
        return None
    return target


def vocabulary_term_name(target: object) -> str | None:
    """Return the human-facing canonical term name for a merge target."""

    canonical = canonical_vocabulary_term(target)
    if canonical is None:
        return None
    names = [
        record.value
        for record in information_of(canonical)
        if record.type is TermName
    ]
    return names[0] if len(names) == 1 else None


S = TypeVar("S")


def _direct_nested_classes(parent: type[object]):
    prefix = parent.__qualname__ + "."
    for value in vars(parent).values():
        if not isinstance(value, type):
            continue
        if value.__module__ != parent.__module__:
            continue
        if not value.__qualname__.startswith(prefix):
            continue
        remainder = value.__qualname__[len(prefix) :]
        if "." in remainder or "<locals>" in remainder:
            continue
        yield value


def _term_declaration(subject: object) -> tuple[str, str] | None:
    """Return ``(term name, definition)`` for a valid declaration docstring.

    A vocabulary term declaration is deliberately tiny: the normalized class
    docstring must begin with exactly one ``{{term name}}`` marker.  Normalization
    uses :func:`inspect.cleandoc`, so Python source indentation is not semantic.
    The rest of the docstring is the definition.  Escaped markers and markers
    appearing later in prose are therefore ordinary text rather than declarations.
    """

    raw = getattr(subject, "__doc__", None)
    if not isinstance(raw, str):
        return None

    normalized = cleandoc(raw)
    if not normalized.startswith("{{"):
        return None

    end = normalized.find("}}", 2)
    if end < 0:
        return None

    declaration = normalized[: end + 2]
    if "\n" in declaration or "\r" in declaration:
        return None

    name = normalized[2:end]
    if (
        not name
        or name != name.strip()
        or "{" in name
        or "}" in name
    ):
        return None

    remainder = normalized[end + 2 :]
    if remainder and not remainder.startswith(("\n", "\r\n")):
        return None

    return name, remainder.lstrip("\r\n").rstrip()


class VocabularyWriter:
    """Mark one canonical source as a Vocabulary semantic profile.

    The marker does not introduce a separate document grammar.  It interprets
    each direct nested class as a term entry whose normalized docstring must begin
    with ``{{term name}}``.  That declaration is projected to semantic ``TermName``
    and ``Definition`` information for validation and Vocabulary realizers.
    """

    __slots__ = ()

    def __call__(self, subject: S) -> S:
        if not isinstance(subject, type):
            raise TypeError("@vocabulary requires a class")
        record_descriptor_use(subject, self)
        attach_information(subject, VocabularyProfile, True)

        for child in _direct_nested_classes(subject):
            declaration = _term_declaration(child)
            if declaration is None:
                continue
            name, definition = declaration
            attach_information(child, TermName, name)
            attach_information(child, Definition, definition)
        return subject


vocabulary = VocabularyWriter()
preserve_spelling = assignment(PreserveSpelling)
glossary = assignment(Glossary)
alias = assignment(Alias)
deprecated = assignment(Deprecated)
replacement = assignment(Replacement)


def _vocabulary_roots(view):
    return [
        item
        for item in view.entities
        if item.values(VocabularyProfile) == (True,)
    ]


def _validate_vocabulary_container(view):
    """Validate a module/package containing one marked Vocabulary root."""

    roots = _vocabulary_roots(view)
    if len(roots) != 1:
        yield Diagnostic(
            "vocabulary descriptions require exactly one @vocabulary canonical source",
            code="vocabulary.document.required",
        )
        return

    root = roots[0]
    for info_type, code, message in (
        (CanonicalSource, "vocabulary.canonical_source.required", "vocabulary root requires exactly one canonical source"),
        (CanonicalTitle, "vocabulary.title.required", "vocabulary root requires exactly one canonical title"),
        (CanonicalContent, "vocabulary.introduction.required", "vocabulary root requires exactly one introduction"),
        (CanonicalFilename, "vocabulary.filename.required", "vocabulary root requires exactly one canonical filename"),
        (CanonicalDocumentPath, "vocabulary.path.required", "vocabulary root requires exactly one logical document path"),
        (CanonicalPlaceholders, "vocabulary.placeholders.required", "vocabulary root requires exactly one placeholder policy"),
        (CanonicalUnreferencedFields, "vocabulary.fields.policy.required", "vocabulary root requires exactly one unreferenced-field policy"),
        (CanonicalHeadingPolicy, "vocabulary.heading.required", "vocabulary root requires exactly one heading policy"),
    ):
        if len(root.values(info_type)) != 1:
            yield Diagnostic(message, code=code, subject=root.subject)


def _validate_vocabulary_relationships(view):
    roots = _vocabulary_roots(view)
    if len(roots) != 1:
        return

    root = roots[0]
    entries = [item for item in view.entities if item.node.parent is root.subject]
    term_by_subject = {
        item.subject: item
        for item in entries
        if len(item.values(TermName)) == 1
    }

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
    yield from _validate_vocabulary_container(view)
    yield from _validate_vocabulary_relationships(view)


@validator(focus=StructuralKind.PACKAGE)
def vocabulary_package(view):
    yield from _validate_vocabulary_container(view)
    yield from _validate_vocabulary_relationships(view)


@validator(focus=StructuralKind.ENTITY)
def vocabulary_entity(view):
    """Validate the marked vocabulary root and term entries."""

    entry = view.focused

    if entry.values(VocabularyProfile):
        if entry.values(VocabularyProfile) != (True,):
            yield Diagnostic(
                "vocabulary root requires exactly one @vocabulary marker",
                code="vocabulary.profile.required",
                subject=entry.subject,
            )
        if any(
            entry.values(info_type)
            for info_type in (Alias, Deprecated, Replacement, PreserveSpelling, Glossary)
        ):
            yield Diagnostic(
                "term metadata belongs on vocabulary entries, not the vocabulary root",
                code="vocabulary.term_metadata.entry_only",
                subject=entry.subject,
            )

        direct_children = [
            item for item in view.entities if item.node.parent is entry.subject
        ]
        if not direct_children:
            yield Diagnostic(
                "vocabulary root requires at least one term entry",
                code="vocabulary.entries.required",
                subject=entry.subject,
            )
        for child in direct_children:
            if _term_declaration(child.subject) is None:
                yield Diagnostic(
                    "normalized vocabulary term docstrings must begin with {{term name}}",
                    code="vocabulary.term.declaration",
                    subject=child.subject,
                )
            elif len(child.values(TermName)) != 1:
                yield Diagnostic(
                    "vocabulary term declaration must produce exactly one term name",
                    code="vocabulary.term.required",
                    subject=child.subject,
                )
        return

    is_term = bool(entry.values(TermName)) or any(
        entry.values(info_type)
        for info_type in (Definition, Alias, Deprecated, Replacement, PreserveSpelling, Glossary)
    )
    if is_term:
        declaration = _term_declaration(entry.subject)
        if declaration is None:
            yield Diagnostic(
                "normalized vocabulary term docstrings must begin with {{term name}}",
                code="vocabulary.term.declaration",
                subject=entry.subject,
            )
            return

        if len(entry.values(TermName)) != 1:
            yield Diagnostic(
                "vocabulary entries require exactly one term name",
                code="vocabulary.term.required",
                subject=entry.subject,
            )
        definitions = entry.values(Definition)
        if len(definitions) != 1 or not definitions[0].strip():
            yield Diagnostic(
                "vocabulary entries require a non-empty definition after the declaration",
                code="vocabulary.definition.required",
                subject=entry.subject,
            )
        if entry.values(CanonicalSource):
            yield Diagnostic(
                "canonical source belongs on the vocabulary root",
                code="vocabulary.canonical_source.root_only",
                subject=entry.subject,
            )
        for value in entry.values(Deprecated):
            if value is False:
                yield Diagnostic(
                    "omit deprecated metadata instead of writing deprecated @= False",
                    code="vocabulary.deprecated.false",
                    subject=entry.subject,
                )


_entity = StructureSelector(kind=StructuralKind.ENTITY)

vocabulary_system = Shikumi(
    structure=PackageTreeStructure(),
    information_types=[
        VocabularyProfile,
        TermName,
        Definition,
        PreserveSpelling,
        Glossary,
        Alias,
        Deprecated,
        Replacement,
        CanonicalSource,
        CanonicalTitle,
        CanonicalContent,
        CanonicalDocumentPath,
        CanonicalFilename,
        CanonicalHeadingPolicy,
        CanonicalPlaceholders,
        CanonicalUnreferencedFields,
    ],
    descriptor_rules=[
        DescriptorUseRule(descriptor=vocabulary, allowed=_entity, name="vocabulary"),
        DescriptorUseRule(descriptor=canonical_source, allowed=_entity, name="canonical_source"),
        DescriptorUseRule(descriptor=preserve_spelling, allowed=_entity, name="preserve_spelling"),
        DescriptorUseRule(descriptor=glossary, allowed=_entity, name="glossary"),
        DescriptorUseRule(descriptor=alias, allowed=_entity, name="alias"),
        DescriptorUseRule(descriptor=deprecated, allowed=_entity, name="deprecated"),
        DescriptorUseRule(descriptor=replacement, allowed=_entity, name="replacement"),
    ],
    validators=[
        information_type_rule(VocabularyProfile),
        information_type_rule(TermName),
        information_type_rule(Definition),
        information_type_rule(PreserveSpelling),
        information_type_rule(Glossary),
        information_type_rule(Alias),
        information_type_rule(Deprecated),
        information_type_rule(Replacement),
        information_type_rule(CanonicalSource),
        information_type_rule(CanonicalTitle),
        information_type_rule(CanonicalContent),
        information_type_rule(CanonicalDocumentPath),
        information_type_rule(CanonicalFilename),
        information_type_rule(CanonicalPlaceholders),
        information_type_rule(CanonicalUnreferencedFields),
        information_type_rule(CanonicalHeadingPolicy),
        vocabulary_module,
        vocabulary_package,
        vocabulary_entity,
    ],
)
