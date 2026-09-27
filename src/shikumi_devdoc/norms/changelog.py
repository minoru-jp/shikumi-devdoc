"""Reusable regulation for structured project changelogs."""

from __future__ import annotations

from enum import Enum
from inspect import cleandoc
import re
from types import ModuleType
from typing import Iterable, TypeVar

from shikumi import (
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
from shikumi.standard import PackageTreeStructure, assignment, information_type_rule

from .common import (
    CanonicalSource,
    VocabularyReference,
    VocabularySource,
    canonical,
    vocabulary,
    vocabulary_reference_diagnostics,
    vocabulary_refs,
)


ChangelogTitle = InformationType("changelog title", str)
Introduction = InformationType("changelog introduction", str)
ReleaseLabel = InformationType("release label", str)
ReleaseNotes = InformationType("release notes", str)
ReleaseDate = InformationType("release date", str)
ChangeKindInformation = InformationType("change kind", object)
ChangeContent = InformationType("change content", str)
Unreleased = InformationType("unreleased", bool)
Breaking = InformationType("breaking", bool)
ChangelogPartOrder = InformationType("changelog part order", int)


class ChangeKind(str, Enum):
    """Categories rendered by the changelog Markdown realizer."""

    ADDED = "Added"
    CHANGED = "Changed"
    DEPRECATED = "Deprecated"
    REMOVED = "Removed"
    FIXED = "Fixed"
    SECURITY = "Security"


ADDED = ChangeKind.ADDED
CHANGED = ChangeKind.CHANGED
DEPRECATED = ChangeKind.DEPRECATED
REMOVED = ChangeKind.REMOVED
FIXED = ChangeKind.FIXED
SECURITY = ChangeKind.SECURITY


S = TypeVar("S")
_RELEASE_CLASS_NAME = re.compile(r"RELEASE_[0-9]+\Z")
_CHANGE_CLASS_NAME = re.compile(r"CHANGE_[0-9]+\Z")
_PART_CLASS_NAME = re.compile(r"CHANGELOG_PART\Z")
_RELEASE_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")


def _docstring(subject: object) -> str:
    raw = getattr(subject, "__doc__", None)
    if not isinstance(raw, str):
        return ""
    return cleandoc(raw)


class ChangelogWriter:
    """Describe the changelog root using a title and root docstring."""

    __slots__ = ()

    def __call__(self, value: str):
        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            attach_information(subject, ChangelogTitle, value)
            attach_information(subject, Introduction, _docstring(subject))
            return subject

        return apply


class ReleaseWriter:
    """Describe one released or unreleased section and its optional notes."""

    __slots__ = ()

    def __call__(self, value: str | None = None):
        if value is not None and not isinstance(value, str):
            raise TypeError("release label must be a string or None")

        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            if value is not None:
                attach_information(subject, ReleaseLabel, value)
            attach_information(subject, ReleaseNotes, _docstring(subject))
            return subject

        return apply


class ChangelogPartWriter:
    """Group physically separated release entries into one logical changelog."""

    __slots__ = ()

    def __call__(self, *, order: int):
        if isinstance(order, bool) or not isinstance(order, int):
            raise TypeError("changelog part order must be an integer")
        if order < 0:
            raise ValueError("changelog part order must be non-negative")

        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            attach_information(subject, ChangelogPartOrder, order)
            return subject

        return apply


class ChangeWriter:
    """Describe one changelog entry using its category and class docstring."""

    __slots__ = ()

    def __call__(self, kind: ChangeKind):
        if not isinstance(kind, ChangeKind):
            raise TypeError("change kind must be a ChangeKind")

        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            attach_information(subject, ChangeKindInformation, kind)
            attach_information(subject, ChangeContent, _docstring(subject))
            return subject

        return apply


changelog = ChangelogWriter()
release = ReleaseWriter()
change = ChangeWriter()
changelog_part = ChangelogPartWriter()
released_on = assignment(ReleaseDate)
unreleased = assignment(Unreleased)
breaking = assignment(Breaking)


def _direct_children(view, subject: object):
    return [item for item in view.entities if item.node.parent is subject]


def _top_level(view, information_type):
    return [
        item
        for item in view.entities
        if isinstance(item.node.parent, ModuleType) and item.has(information_type)
    ]


def _part_order(item) -> int:
    values = item.values(ChangelogPartOrder)
    if len(values) != 1 or isinstance(values[0], bool) or not isinstance(values[0], int):
        return 0
    return values[0]


def _ordered_parts(view):
    return sorted(
        _top_level(view, ChangelogPartOrder),
        key=lambda item: (_part_order(item), item.node.path),
    )


def _ordered_releases(view, root):
    releases = [
        item for item in _direct_children(view, root.subject) if item.has(ReleaseNotes)
    ]
    for part in _ordered_parts(view):
        releases.extend(
            item for item in _direct_children(view, part.subject) if item.has(ReleaseNotes)
        )
    return releases


def _validate_release_children(view, release_item):
    changes = _direct_children(view, release_item.subject)
    if not changes:
        yield Diagnostic(
            "release entries require at least one change entry",
            code="changelog.change.required",
            subject=release_item.subject,
        )
    for child in changes:
        if len(child.values(ChangeKindInformation)) != 1:
            yield Diagnostic(
                "release children must be change entries",
                code="changelog.change.child",
                subject=child.subject,
            )
        if _direct_children(view, child.subject):
            yield Diagnostic(
                "change entries must not contain nested entities",
                code="changelog.change.leaf",
                subject=child.subject,
            )


def _validate_changelog_container(view):
    roots = _top_level(view, ChangelogTitle)
    if len(roots) != 1:
        yield Diagnostic(
            "changelog descriptions require exactly one changelog root",
            code="changelog.root.required",
        )
        return

    root = roots[0]
    if len(root.values(CanonicalSource)) != 1:
        yield Diagnostic(
            "changelog root requires exactly one canonical source",
            code="changelog.canonical_source.required",
            subject=root.subject,
        )
    if root.node.name != "CHANGELOG":
        yield Diagnostic(
            "changelog root entity must be named CHANGELOG",
            code="changelog.root.name",
            subject=root.subject,
        )

    root_children = _direct_children(view, root.subject)
    for child in root_children:
        if len(child.values(ReleaseNotes)) != 1:
            yield Diagnostic(
                "changelog root children must be release entries",
                code="changelog.release.child",
                subject=child.subject,
            )

    parts = _ordered_parts(view)
    orders: dict[int, object] = {}
    for part in parts:
        order = _part_order(part)
        previous = orders.get(order)
        if previous is not None:
            yield Diagnostic(
                f"changelog part order {order} is already used",
                code="changelog.part.order.duplicate",
                subject=part.subject,
            )
        else:
            orders[order] = part.subject

        children = _direct_children(view, part.subject)
        if not children:
            yield Diagnostic(
                "changelog parts require at least one release entry",
                code="changelog.part.release.required",
                subject=part.subject,
            )
        for child in children:
            if len(child.values(ReleaseNotes)) != 1:
                yield Diagnostic(
                    "changelog part children must be release entries",
                    code="changelog.part.release.child",
                    subject=child.subject,
                )

    releases = _ordered_releases(view, root)
    if not releases:
        yield Diagnostic(
            "changelog requires at least one release",
            code="changelog.release.required",
            subject=root.subject,
        )

    logical_release_ids = {id(item.subject) for item in releases}
    for item in view.entities:
        if item.has(ReleaseNotes) and id(item.subject) not in logical_release_ids:
            yield Diagnostic(
                "release entries must be direct children of CHANGELOG or CHANGELOG_PART",
                code="changelog.release.parent",
                subject=item.subject,
            )

    labels: dict[str, object] = {}
    for release_item in releases:
        if release_item.values(Unreleased) == (True,):
            continue
        values = release_item.values(ReleaseLabel)
        if len(values) != 1:
            continue
        label = values[0]
        previous = labels.get(label)
        if previous is not None:
            yield Diagnostic(
                f"release label {label!r} is already used",
                code="changelog.release.label.duplicate",
                subject=release_item.subject,
            )
        else:
            labels[label] = release_item.subject

    unreleased_entries = [item for item in releases if item.values(Unreleased) == (True,)]
    if len(unreleased_entries) > 1:
        for item in unreleased_entries[1:]:
            yield Diagnostic(
                "changelog allows at most one unreleased section",
                code="changelog.unreleased.cardinality",
                subject=item.subject,
            )
    if unreleased_entries and releases[0].subject is not unreleased_entries[0].subject:
        yield Diagnostic(
            "the unreleased section must be the first logical release entry",
            code="changelog.unreleased.order",
            subject=unreleased_entries[0].subject,
        )

    logical_change_ids: set[int] = set()
    for release_item in releases:
        for child in _direct_children(view, release_item.subject):
            if child.has(ChangeKindInformation):
                logical_change_ids.add(id(child.subject))
        yield from _validate_release_children(view, release_item)

    for item in view.entities:
        if item.has(ChangeKindInformation) and id(item.subject) not in logical_change_ids:
            yield Diagnostic(
                "change entries must be direct children of a logical release entry",
                code="changelog.change.parent",
                subject=item.subject,
            )


@validator(focus=StructuralKind.MODULE)
def changelog_module(view):
    """Validate a standalone changelog module.

    Package validation owns cross-module composition, so module subviews that
    were discovered from a package deliberately skip container validation.
    """

    if isinstance(view.focused.node.parent, ModuleType):
        return
    yield from _validate_changelog_container(view)


@validator(focus=StructuralKind.PACKAGE)
def changelog_package(view):
    """Validate the outer changelog package as one logical container."""

    if isinstance(view.focused.node.parent, ModuleType):
        return
    yield from _validate_changelog_container(view)


@validator(focus=StructuralKind.ENTITY)
def changelog_entity(view):
    """Validate one root, release, or change changelog entity."""

    item = view.focused

    if item.has(ChangelogTitle):
        if len(item.values(ChangelogTitle)) != 1:
            yield Diagnostic(
                "changelog root requires exactly one title",
                code="changelog.title.required",
            )
        if len(item.values(Introduction)) != 1:
            yield Diagnostic(
                "changelog root requires exactly one introduction",
                code="changelog.introduction.required",
            )
        if item.node.name != "CHANGELOG":
            yield Diagnostic(
                "changelog root entity must be named CHANGELOG",
                code="changelog.root.name",
            )
        if len(item.values(CanonicalSource)) != 1:
            yield Diagnostic(
                "changelog root requires exactly one canonical source",
                code="changelog.canonical_source.required",
            )
        if len(item.values(VocabularySource)) > 1:
            yield Diagnostic(
                "changelog root allows at most one vocabulary",
                code="changelog.vocabulary.cardinality",
            )
        if item.values(Unreleased) or item.values(Breaking) or item.values(ChangelogPartOrder):
            yield Diagnostic(
                "entry and part metadata do not belong on the changelog root",
                code="changelog.metadata.entry_only",
            )
        yield from vocabulary_reference_diagnostics(
            item,
            (*item.values(ChangelogTitle), *item.values(Introduction)),
            code_prefix="changelog",
        )
        return

    if item.has(ChangelogPartOrder):
        if _PART_CLASS_NAME.fullmatch(item.node.name) is None:
            yield Diagnostic(
                "changelog part class must be named CHANGELOG_PART",
                code="changelog.part.name",
            )
        if not isinstance(item.node.parent, ModuleType):
            yield Diagnostic(
                "changelog parts must be top-level classes in a module",
                code="changelog.part.top_level",
            )
        orders = item.values(ChangelogPartOrder)
        if len(orders) != 1:
            yield Diagnostic(
                "changelog parts require exactly one order",
                code="changelog.part.order.required",
            )
        for order in orders:
            if isinstance(order, bool) or not isinstance(order, int) or order < 0:
                yield Diagnostic(
                    "changelog part order must be a non-negative integer",
                    code="changelog.part.order.value",
                )
        if item.values(CanonicalSource) or item.values(VocabularySource):
            yield Diagnostic(
                "canonical source and vocabulary belong on the changelog root",
                code="changelog.part.root_metadata",
            )
        if item.values(Unreleased) or item.values(Breaking):
            yield Diagnostic(
                "unreleased and breaking metadata belong on release or change entries",
                code="changelog.part.entry_metadata",
            )
        return

    if item.values(CanonicalSource):
        yield Diagnostic(
            "canonical source belongs on the changelog root",
            code="changelog.canonical_source.root_only",
        )

    if item.values(VocabularySource):
        yield Diagnostic(
            "vocabulary belongs on the changelog root",
            code="changelog.vocabulary.root_only",
        )

    if item.has(ReleaseNotes):
        if _RELEASE_CLASS_NAME.fullmatch(item.node.name) is None:
            yield Diagnostic(
                "release class names must match RELEASE_<decimal digits>",
                code="changelog.release.name",
            )
        is_unreleased = item.values(Unreleased) == (True,)
        labels = item.values(ReleaseLabel)
        if is_unreleased:
            if labels:
                yield Diagnostic(
                    "unreleased sections use @release() without a label",
                    code="changelog.unreleased.label",
                )
        elif len(labels) != 1:
            yield Diagnostic(
                "released entries require exactly one label",
                code="changelog.release.label",
            )
        if len(item.values(ReleaseNotes)) != 1:
            yield Diagnostic(
                "release entries require exactly one notes body",
                code="changelog.release.notes",
            )
        for value in item.values(Unreleased):
            if value is False:
                yield Diagnostic(
                    "omit unreleased metadata instead of writing unreleased @= False",
                    code="changelog.unreleased.false",
                )
        if item.values(Breaking):
            yield Diagnostic(
                "breaking metadata belongs on change entries",
                code="changelog.breaking.change_only",
            )
        if item.values(ChangelogPartOrder):
            yield Diagnostic(
                "changelog part order belongs on CHANGELOG_PART",
                code="changelog.part.order.part_only",
            )
        dates = item.values(ReleaseDate)
        if is_unreleased and dates:
            yield Diagnostic(
                "unreleased sections must not have a release date",
                code="changelog.unreleased.date",
            )
        if len(dates) > 1:
            yield Diagnostic(
                "release entries allow at most one release date",
                code="changelog.release.date.cardinality",
            )
        for value in dates:
            if _RELEASE_DATE.fullmatch(value) is None:
                yield Diagnostic(
                    "release dates must use YYYY-MM-DD",
                    code="changelog.release.date.format",
                )
        yield from vocabulary_reference_diagnostics(
            item,
            (*item.values(ReleaseLabel), *item.values(ReleaseNotes)),
            code_prefix="changelog",
        )
        return

    if item.has(ChangeKindInformation):
        if _CHANGE_CLASS_NAME.fullmatch(item.node.name) is None:
            yield Diagnostic(
                "change class names must match CHANGE_<decimal digits>",
                code="changelog.change.name",
            )
        kinds = item.values(ChangeKindInformation)
        if len(kinds) != 1 or not isinstance(kinds[0], ChangeKind):
            yield Diagnostic(
                "change entries require exactly one ChangeKind",
                code="changelog.change.kind",
            )
        contents = item.values(ChangeContent)
        if len(contents) != 1 or not contents[0].strip():
            yield Diagnostic(
                "change entries require one non-empty content body",
                code="changelog.change.content",
            )
        if item.values(Unreleased):
            yield Diagnostic(
                "unreleased metadata belongs on release entries",
                code="changelog.unreleased.release_only",
            )
        if item.values(ChangelogPartOrder):
            yield Diagnostic(
                "changelog part order belongs on CHANGELOG_PART",
                code="changelog.part.order.part_only",
            )
        for value in item.values(Breaking):
            if value is False:
                yield Diagnostic(
                    "omit breaking metadata instead of writing breaking @= False",
                    code="changelog.breaking.false",
                )
        yield from vocabulary_reference_diagnostics(
            item,
            contents,
            code_prefix="changelog",
        )
        return

    yield Diagnostic(
        "changelog entities must be the root, a release, or a change entry",
        code="changelog.entity.kind",
    )


_entity = StructureSelector(kind=StructuralKind.ENTITY)

changelog_system = Shikumi(
    structure=PackageTreeStructure(),
    information_types=[
        ChangelogTitle,
        Introduction,
        ReleaseLabel,
        ReleaseNotes,
        ReleaseDate,
        ChangeKindInformation,
        ChangeContent,
        Unreleased,
        Breaking,
        ChangelogPartOrder,
        VocabularySource,
        VocabularyReference,
        CanonicalSource,
    ],
    descriptor_rules=[
        DescriptorUseRule(descriptor=changelog, allowed=_entity, name="changelog"),
        DescriptorUseRule(descriptor=canonical, allowed=_entity, name="canonical"),
        DescriptorUseRule(descriptor=release, allowed=_entity, name="release"),
        DescriptorUseRule(descriptor=change, allowed=_entity, name="change"),
        DescriptorUseRule(descriptor=changelog_part, allowed=_entity, name="changelog_part"),
        DescriptorUseRule(descriptor=released_on, allowed=_entity, name="released_on"),
        DescriptorUseRule(descriptor=unreleased, allowed=_entity, name="unreleased"),
        DescriptorUseRule(descriptor=breaking, allowed=_entity, name="breaking"),
        DescriptorUseRule(descriptor=vocabulary, allowed=_entity, name="vocabulary"),
        DescriptorUseRule(
            descriptor=vocabulary_refs,
            allowed=_entity,
            name="vocabulary_refs",
        ),
    ],
    validators=[
        information_type_rule(ChangelogTitle),
        information_type_rule(Introduction),
        information_type_rule(ReleaseLabel),
        information_type_rule(ReleaseNotes),
        information_type_rule(ReleaseDate),
        information_type_rule(ChangeKindInformation),
        information_type_rule(ChangeContent),
        information_type_rule(Unreleased),
        information_type_rule(Breaking),
        information_type_rule(ChangelogPartOrder),
        information_type_rule(VocabularySource),
        information_type_rule(VocabularyReference),
        information_type_rule(CanonicalSource),
        changelog_module,
        changelog_package,
        changelog_entity,
    ],
)
