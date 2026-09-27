"""Shared information and authoring decorators used across devdoc regulations."""

from __future__ import annotations

from pathlib import Path
import sys
from types import ModuleType
from typing import Iterable, TypeVar

from shikumi import Cardinality, Diagnostic, InformationType, attach_information, record_descriptor_use

from shikumi_devdoc._placeholder_syntax import placeholder_keys


CanonicalSource = InformationType("canonical source", str)
VocabularySource = InformationType("vocabulary source", ModuleType)
VocabularyReference = InformationType("vocabulary reference", type, cardinality=Cardinality.MANY)


_VOCABULARY_SOURCE_ATTRIBUTE = "__shikumi_devdoc_vocabulary_source__"
_VOCABULARY_TARGET_ATTRIBUTE = "__shikumi_devdoc_vocabulary_target__"


def vocabulary_reference_diagnostics(item, texts: Iterable[str], *, code_prefix: str):
    """Validate local TERM markers against this entity's explicit vocabulary refs.

    TERM markers are intentionally checked per entity.  Parent and child entities do
    not inherit references from one another.  External-context placeholders such as
    ``{{PROJECT.version}}`` are outside this validation.
    """

    used = {
        key
        for text in texts
        if isinstance(text, str)
        for key in placeholder_keys(text)
        if key.startswith("TERM_") and key[5:].isdigit()
    }
    referenced = {
        getattr(reference, "__name__", "")
        for reference in item.values(VocabularyReference)
    }

    for marker in sorted(used - referenced):
        yield Diagnostic(
            f"{marker} is used by this entity but missing from vocabulary_refs",
            code=f"{code_prefix}.vocabulary_reference.missing",
            subject=item.subject,
        )

    for marker in sorted(referenced - used):
        yield Diagnostic(
            f"{marker} is listed in vocabulary_refs but not used by this entity",
            code=f"{code_prefix}.vocabulary_reference.unused",
            subject=item.subject,
        )

S = TypeVar("S")


class CanonicalDecorator:
    """Declare the decorated root entity as the canonical source of its artifact."""

    __slots__ = ()

    def __call__(self, subject: S) -> S:
        record_descriptor_use(subject, self)
        attach_information(subject, CanonicalSource, _source_path_for_subject(subject))
        return subject


class VocabularyDecorator:
    """Connect a generated term-reference module to a document-like root entity."""

    __slots__ = ()

    def __call__(self, reference_module: ModuleType):
        source = _canonical_vocabulary_source(reference_module)

        def apply(subject: S) -> S:
            record_descriptor_use(subject, self)
            attach_information(subject, VocabularySource, source)
            return subject

        return apply


class VocabularyReferencesWriter:
    """Attach direct Python references to vocabulary entities for navigation."""

    __slots__ = ()

    def __imatmul__(self, value: Iterable[type[object]]) -> object:
        from shikumi import class_binding

        references = tuple(_canonical_vocabulary_reference(reference) for reference in value)
        return class_binding(references, self._connect)

    def _connect(self, subject: type[object], references: tuple[type[object], ...]) -> None:
        record_descriptor_use(subject, self)
        for reference in references:
            attach_information(subject, VocabularyReference, reference)


def _canonical_vocabulary_source(reference_module: ModuleType) -> ModuleType:
    if not isinstance(reference_module, ModuleType):
        raise TypeError("vocabulary() requires a Python module")

    source = getattr(reference_module, _VOCABULARY_SOURCE_ATTRIBUTE, reference_module)
    if not isinstance(source, ModuleType):
        raise TypeError("generated term-reference module has an invalid vocabulary source")
    if not hasattr(source, "VOCABULARY"):
        raise TypeError(
            "vocabulary() requires a generated term-reference module or a canonical vocabulary module"
        )
    return source


def _source_path_for_subject(subject: object) -> str:
    module_name = getattr(subject, "__module__", "")
    module = sys.modules.get(module_name)
    raw = getattr(module, "__file__", None) if module is not None else None
    if raw:
        path = Path(raw).resolve()
        try:
            return path.relative_to(Path.cwd().resolve()).as_posix()
        except ValueError:
            pass
    if module_name and module_name != "__main__":
        return module_name.replace(".", "/") + ".py"
    return str(raw or module_name or "unknown source")


def _canonical_vocabulary_reference(reference: type[object]) -> type[object]:
    """Resolve generated term-reference proxies back to canonical vocabulary classes."""

    if not isinstance(reference, type):
        raise TypeError("vocabulary references must be classes")
    target = getattr(reference, _VOCABULARY_TARGET_ATTRIBUTE, reference)
    if not isinstance(target, type):
        raise TypeError("generated vocabulary reference target must be a class")
    return target


canonical = CanonicalDecorator()
vocabulary = VocabularyDecorator()
vocabulary_refs = VocabularyReferencesWriter()
