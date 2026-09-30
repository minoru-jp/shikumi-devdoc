"""Shared information and authoring decorators used across devdoc regulations."""

from __future__ import annotations

from enum import Enum
from inspect import cleandoc
import keyword
from pathlib import Path, PurePosixPath
import sys
import warnings
from types import ModuleType
from typing import TypeVar

from shikumi import Cardinality, InformationType, attach_information, record_descriptor_use

from ._partitioned import validate_filename, validate_optional_order


CanonicalSource = InformationType("canonical source", str)
CanonicalTitle = InformationType("canonical title", str)
CanonicalSummary = InformationType("canonical summary", str)
CanonicalContent = InformationType("canonical content", str)
CanonicalFilename = InformationType("canonical filename", str)
CanonicalDocumentPath = InformationType("canonical document path", str)
CanonicalOrder = InformationType("canonical order", int)


class MergePolicy(str, Enum):
    """Which explicit merge/context sources a canonical document may use."""

    ALL = "all"
    LOCAL = "local"
    EXTERNAL = "external"
    FORBIDDEN = "forbidden"

    @property
    def allows_local(self) -> bool:
        """Whether explicit local ``merge @= ...`` declarations are allowed."""
        return self in (MergePolicy.ALL, MergePolicy.LOCAL)

    @property
    def allows_external(self) -> bool:
        return self in (MergePolicy.ALL, MergePolicy.EXTERNAL)


CanonicalMergePolicy = InformationType("canonical merge policy", MergePolicy)
MergeBinding = InformationType("merge binding", tuple, cardinality=Cardinality.MANY)


class UnreferencedFieldPolicy(str, Enum):
    """How a canonical document handles fields absent from its body template."""

    APPEND = "append"
    IGNORE = "ignore"


APPEND = UnreferencedFieldPolicy.APPEND
IGNORE = UnreferencedFieldPolicy.IGNORE
CanonicalUnreferencedFields = InformationType(
    "canonical unreferenced fields",
    UnreferencedFieldPolicy,
)


class HeadingPolicy(str, Enum):
    """How nested document nodes become Markdown headings."""

    TITLE = "title"
    IDENTITY = "identity"


CanonicalHeadingPolicy = InformationType(
    "canonical heading policy",
    HeadingPolicy,
)


S = TypeVar("S")


class ShikumiDevdocDeprecationWarning(DeprecationWarning):
    """Deprecation warning emitted by shikumi-devdoc public APIs."""


class _Unspecified:
    __slots__ = ()

    def __repr__(self) -> str:
        return "<unspecified>"


_UNSPECIFIED = _Unspecified()


def _docstring(subject: object) -> str:
    raw = getattr(subject, "__doc__", None)
    if not isinstance(raw, str):
        return ""
    return cleandoc(raw)


def _nonempty_string(value: str, *, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string")
    if not value.strip():
        raise ValueError(f"{label} must be non-empty")
    return value


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


def _attach_document_content(parent: type[object]) -> None:
    """Capture docstrings for every lexical child of a canonical document root."""

    for child in _direct_nested_classes(parent):
        attach_information(child, CanonicalContent, _docstring(child))
        _attach_document_content(child)


class CanonicalSourceDecorator:
    """Declare a canonical source unit and optional canonical-document metadata.

    Bare ``@canonical_source`` marks non-document canonical sources.
    ``@canonical_source(...)`` declares a canonical document root. Document
    structure is common: lexical child classes are document nodes and their
    docstrings are captured as template content.
    """

    __slots__ = ()

    def __call__(
        self,
        subject_or_title=None,
        *,
        filename: str | None = None,
        order: int | None = None,
        placeholders: bool | _Unspecified = _UNSPECIFIED,
        merge_policy: str | MergePolicy | _Unspecified = _UNSPECIFIED,
        unreferenced_fields: UnreferencedFieldPolicy = APPEND,
        heading: str | HeadingPolicy | None = None,
    ):
        if isinstance(subject_or_title, type):
            if (
                filename is not None
                or order is not None
                or placeholders is not _UNSPECIFIED
                or merge_policy is not _UNSPECIFIED
                or unreferenced_fields is not APPEND
                or heading is not None
            ):
                raise TypeError("bare @canonical_source does not accept document metadata")
            return self._apply_source(subject_or_title)

        if subject_or_title is None:
            raise TypeError("canonical_source() requires a document title")
        title = _nonempty_string(subject_or_title, label="canonical title")
        if filename is None:
            raise TypeError("canonical_source() requires filename= for canonical documents")
        filename = validate_filename(filename, label="canonical filename")
        order = validate_optional_order(order, label="canonical order")
        if placeholders is not _UNSPECIFIED and merge_policy is not _UNSPECIFIED:
            raise TypeError("canonical_source() cannot specify both placeholders= and merge_policy=")
        if placeholders is not _UNSPECIFIED:
            if not isinstance(placeholders, bool):
                raise TypeError("canonical placeholders policy must be a bool")
            effective_merge_policy = MergePolicy.ALL if placeholders else MergePolicy.LOCAL
            warnings.warn(
                f"'placeholders={placeholders}' is deprecated and will be removed in 1.0.0; "
                f"use 'merge_policy=\"{effective_merge_policy.value}\"' instead.",
                ShikumiDevdocDeprecationWarning,
                stacklevel=2,
            )
        else:
            if merge_policy is _UNSPECIFIED:
                effective_merge_policy = MergePolicy.ALL
            else:
                try:
                    effective_merge_policy = MergePolicy(merge_policy)
                except (TypeError, ValueError) as exc:
                    raise ValueError(
                        'canonical merge_policy must be "all", "local", "external", or "forbidden"'
                    ) from exc
        if not isinstance(unreferenced_fields, UnreferencedFieldPolicy):
            raise TypeError("canonical unreferenced_fields must be APPEND or IGNORE")
        if heading is None:
            raise TypeError('canonical_source() requires heading="title" or heading="identity"')
        try:
            heading_policy = HeadingPolicy(heading)
        except (TypeError, ValueError) as exc:
            raise ValueError('canonical heading must be "title" or "identity"') from exc

        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            source_path = _source_path_for_subject(subject)
            attach_information(subject, CanonicalSource, source_path)
            attach_information(subject, CanonicalTitle, title)
            attach_information(subject, CanonicalContent, _docstring(subject))
            attach_information(subject, CanonicalFilename, filename)
            attach_information(
                subject,
                CanonicalDocumentPath,
                _document_path_for_source(source_path, filename),
            )
            if order is not None:
                attach_information(subject, CanonicalOrder, order)
            attach_information(subject, CanonicalMergePolicy, effective_merge_policy)
            attach_information(subject, CanonicalUnreferencedFields, unreferenced_fields)
            attach_information(subject, CanonicalHeadingPolicy, heading_policy)
            if isinstance(subject, type):
                _attach_document_content(subject)
            return subject

        return apply

    def _apply_source(self, subject: S) -> S:
        record_descriptor_use(subject, self)
        attach_information(subject, CanonicalSource, _source_path_for_subject(subject))
        return subject


class SummaryDecorator:
    """Attach a concise human-facing summary to one canonical source."""

    __slots__ = ()

    def __call__(self, value: str):
        value = _nonempty_string(value, label="canonical summary")

        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            attach_information(subject, CanonicalSummary, value)
            return subject

        return apply


def _normalize_merge_value(value: object) -> tuple[object, object]:
    if isinstance(value, tuple) and len(value) == 2:
        name, target = value
        if not isinstance(name, str):
            raise TypeError("merge name must be a string")
        if not name.isidentifier() or keyword.iskeyword(name):
            raise ValueError("merge name must be a non-keyword Python identifier")
        return name, target
    if isinstance(value, type):
        return None, value
    raise TypeError(
        'merge requires a class target or an explicit ("name", target) tuple'
    )


class _MergeClassBinding:
    """Temporary class-body binding that normalizes every repeated merge write."""

    __slots__ = ("values", "connect")

    def __init__(self, values, connect) -> None:
        self.values = tuple(values)
        self.connect = connect

    def __imatmul__(self, value: object):
        return _MergeClassBinding(
            (*self.values, _normalize_merge_value(value)),
            self.connect,
        )

    def __set_name__(self, owner: type[object], name: str) -> None:
        for value in self.values:
            self.connect(owner, value)
        if owner.__dict__.get(name) is self:
            delattr(owner, name)


class MergeWriter:
    """Bind one local template reference to an explicit realization target.

    ``merge @= target`` adds Python-identity-based names for a class target to
    the node-local template namespace. ``merge @= ("name", target)`` adds an
    explicit alias, including for strings and field bindings. Field ``@=``
    bindings already participate in that namespace without a merge declaration.
    What kinds of targets are realizable is decided by document
    validation/realization rather than by this generic binding writer.
    """

    __slots__ = ()

    def __imatmul__(self, value: object) -> object:
        return _MergeClassBinding((_normalize_merge_value(value),), self._connect)

    def _connect(self, subject: type[object], value: tuple[object, object]) -> None:
        record_descriptor_use(subject, self)
        attach_information(subject, MergeBinding, value)



def _document_path_for_source(source_path: str, filename: str) -> str:
    """Return a stable logical document path from source provenance and filename.

    The path describes canonical-document topology only.  It is independent of
    the realization output directory and any later publication layout.
    """

    source = PurePosixPath(source_path)
    return (source.parent / filename).as_posix()

def _source_path_for_subject(subject: object) -> str:
    module_name = getattr(subject, "__module__", "")
    module = sys.modules.get(module_name)
    if module is not None:
        return _source_path_for_module(module)
    if module_name and module_name != "__main__":
        return module_name.replace(".", "/") + ".py"
    return str(module_name or "unknown source")


def _source_path_for_module(module: ModuleType) -> str:
    """Return stable provenance from the module structure, independent of CWD."""

    module_name = getattr(module, "__name__", "")
    if module_name and module_name != "__main__":
        path = Path(*module_name.split("."))
        spec = getattr(module, "__spec__", None)
        if getattr(spec, "submodule_search_locations", None) is not None:
            return (path / "__init__.py").as_posix()
        return path.with_suffix(".py").as_posix()

    raw = getattr(module, "__file__", None)
    if isinstance(raw, str) and raw:
        return Path(raw).name
    return str(module_name or "unknown source")


canonical_source = CanonicalSourceDecorator()
summary = SummaryDecorator()
merge = MergeWriter()
