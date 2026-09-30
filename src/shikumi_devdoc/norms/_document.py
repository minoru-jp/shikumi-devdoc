"""Generic regulation for canonical developer documents."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import sys
from types import ModuleType
from typing import Any, TypeVar

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
from shikumi.standard import PackageTreeStructure, information_type_rule

from shikumi_devdoc._placeholder_syntax import placeholder_keys
from ._common import (
    CanonicalContent,
    CanonicalDocumentPath,
    CanonicalFilename,
    CanonicalHeadingPolicy,
    CanonicalOrder,
    CanonicalMergePolicy,
    CanonicalSource,
    CanonicalSummary,
    CanonicalTitle,
    CanonicalUnreferencedFields,
    MergeBinding,
    MergePolicy,
    HeadingPolicy,
    canonical_source,
    merge,
    summary,
)
from ._partitioned import filename_value_error


Title = InformationType("document node title", str)


class FieldPresentation(str, Enum):
    """Generic Markdown-oriented presentation selected by a field writer."""

    INLINE = "inline"
    REFERENCE = "reference"
    LIST = "list"
    TABLE = "table"
    TEST_TARGET = "test_target"
    PROSE = "prose"


@dataclass(frozen=True, slots=True)
class FieldValue:
    """One author-defined field value attached to a canonical document node."""

    binding_name: str
    schema: InformationType[Any]
    value: object
    presentation: FieldPresentation
    columns: tuple[str, ...] = ()


DocumentField = InformationType(
    "document field",
    FieldValue,
    cardinality=Cardinality.MANY,
)


S = TypeVar("S")


class _TitleBinding:
    """Temporary class-body binding for one or more ``title @=`` writes."""

    __slots__ = ("writer", "values")

    def __init__(self, writer: "TitleWriter", values: tuple[str, ...]) -> None:
        self.writer = writer
        self.values = values

    def __imatmul__(self, value: str) -> "_TitleBinding":
        self.writer._validate(value)
        return _TitleBinding(self.writer, (*self.values, value))

    def __set_name__(self, owner: type[object], name: str) -> None:
        for value in self.values:
            self.writer._connect(owner, value)
        if owner.__dict__.get(name) is self:
            delattr(owner, name)


class TitleWriter:
    """Write one human-readable document-node title with ``title @= ...``."""

    __slots__ = ()

    @staticmethod
    def _validate(value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("document node title must be a string")
        if not value.strip():
            raise ValueError("document node title must be non-empty")
        if "\n" in value or "\r" in value:
            raise ValueError("document node title must be a single line before template expansion")

    def __imatmul__(self, value: str) -> _TitleBinding:
        self._validate(value)
        return _TitleBinding(self, (value,))

    def _connect(self, subject: type[object], value: str) -> None:
        record_descriptor_use(subject, self)
        attach_information(subject, Title, value)


class _FieldBinding:
    """Temporary class-body binding retaining one concrete assignment identity."""

    __slots__ = ("writer", "values", "binding_name")

    def __init__(self, writer: "FieldWriter", values: tuple[object, ...]) -> None:
        self.writer = writer
        self.values = values
        self.binding_name: str | None = None

    def __imatmul__(self, value: object) -> "_FieldBinding":
        # Keep the same object so an earlier ``merge @= ("alias", binding)``
        # continues to identify this exact field binding after later writes.
        self.values = self.values + (value,)
        return self

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.binding_name = name
        for value in self.values:
            self.writer._connect(owner, name, value)
        if owner.__dict__.get(name) is self:
            delattr(owner, name)


class FieldWriter:
    """Write an author-defined field with ``@=``.

    The canonical display name belongs to ``field(...)`` while the Python
    class-body assignment target is retained independently. Once written, that
    binding name participates automatically in the node-local template namespace.
    A field writer or its temporary class-body binding can also be used as an
    explicit ``merge`` target when an alias is useful.
    """

    __slots__ = ("schema", "presentation", "columns")

    def __init__(
        self,
        name: str,
        value_type: type[Any] | tuple[type[Any], ...] = object,
        *,
        many: bool = False,
        presentation: FieldPresentation = FieldPresentation.INLINE,
        columns: tuple[str, ...] = (),
    ) -> None:
        if not isinstance(name, str):
            raise TypeError("field name must be a string")
        if not name.strip():
            raise ValueError("field name must be non-empty")
        if "\n" in name or "\r" in name:
            raise ValueError("field name must be a single line")
        cardinality = Cardinality.MANY if many else Cardinality.ONE
        self.schema = InformationType(name, value_type, cardinality=cardinality)
        self.presentation = presentation
        self.columns = columns

    @property
    def name(self) -> str:
        return self.schema.name

    @property
    def value_type(self):
        return self.schema.value_type

    @property
    def cardinality(self) -> Cardinality:
        return self.schema.cardinality

    def __imatmul__(self, value: object) -> object:
        return _FieldBinding(self, (value,))

    def _connect(self, subject: type[object], binding_name: str, value: object) -> None:
        record_descriptor_use(subject, self)
        attach_information(
            subject,
            DocumentField,
            FieldValue(
                binding_name,
                self.schema,
                value,
                self.presentation,
                columns=self.columns,
            ),
        )


def field(
    name: str,
    value_type: type[Any] | tuple[type[Any], ...] = object,
    *,
    many: bool = False,
) -> FieldWriter:
    """Create a literal field rendered inline when appended."""

    return FieldWriter(name, value_type, many=many)


def reference_field(
    name: str,
    value_type: type[Any] | tuple[type[Any], ...] = type,
    *,
    many: bool = False,
) -> FieldWriter:
    """Create a semantic-reference field rendered as Markdown links when resolvable."""

    return FieldWriter(
        name,
        value_type,
        many=many,
        presentation=FieldPresentation.REFERENCE,
    )


def list_field(
    name: str,
    value_type: type[Any] | tuple[type[Any], ...] = object,
) -> FieldWriter:
    """Create a repeatable literal field rendered as a Markdown bullet list."""

    return FieldWriter(name, value_type, many=True, presentation=FieldPresentation.LIST)


def test_target_field(
    name: str,
    *,
    many: bool = False,
) -> FieldWriter:
    """Create literal text separated for direct use by ordinary tests.

    The writer does not choose Markdown presentation. Authors place its local
    reference inside the surrounding docstring or prose template, for example
    inside an explicit fenced block. Multiline values are normalized with
    ``inspect.cleandoc()`` when inserted into a template so Python indentation
    does not become part of the test target.
    """

    return FieldWriter(
        name,
        str,
        many=many,
        presentation=FieldPresentation.TEST_TARGET,
    )


# pytest discovers imported module-level callables whose names start with ``test_``.
# This is an authoring factory, not a test function.
test_target_field.__test__ = False


def table_field(
    name: str,
    *,
    columns: tuple[str, ...],
) -> FieldWriter:
    """Create a repeatable literal field rendered as a Markdown table."""

    if not isinstance(columns, tuple):
        raise TypeError("table field columns must be a tuple")
    if not columns:
        raise ValueError("table field requires at least one column")
    normalized: list[str] = []
    for column in columns:
        if not isinstance(column, str):
            raise TypeError("table field column names must be strings")
        if not column.strip():
            raise ValueError("table field column names must be non-empty")
        if "\n" in column or "\r" in column:
            raise ValueError("table field column names must be single-line strings")
        normalized.append(column)
    if len({column.casefold() for column in normalized}) != len(normalized):
        raise ValueError("table field column names must be unique")
    return FieldWriter(
        name,
        (tuple, list),
        many=True,
        presentation=FieldPresentation.TABLE,
        columns=tuple(normalized),
    )


def prose_field(name: str) -> FieldWriter:
    """Create one named Markdown prose template fragment.

    Prose values interpret generic ``{{name}}`` placeholders. Field bindings on
    the same document node are available by their ``@=`` left-hand names, and
    ``merge`` may add class targets, literals, or explicit aliases. Ordinary
    field values remain literal.
    """

    return FieldWriter(name, str, presentation=FieldPresentation.PROSE)


title = TitleWriter()


def _direct_children(view, subject: object):
    return [candidate for candidate in view.entities if candidate.node.parent is subject]


def _document_roots(view):
    return [
        item
        for item in view.entities
        if isinstance(item.node.parent, ModuleType) and item.has(CanonicalTitle)
    ]


def _document_descendants(view, root):
    result = []

    def visit(subject: object) -> None:
        for child in _direct_children(view, subject):
            result.append(child)
            visit(child.subject)

    visit(root.subject)
    return result


def _document_members(view, root):
    return [root, *_document_descendants(view, root)]


def _qualified_class_chain(subject: type[object]) -> tuple[type[object], ...]:
    module = sys.modules.get(subject.__module__)
    if module is None:
        return (subject,)
    parts = [part for part in subject.__qualname__.split(".") if part != "<locals>"]
    current: object = module
    classes: list[type[object]] = []
    for part in parts:
        current = getattr(current, part, None)
        if current is None:
            return (subject,)
        if isinstance(current, type):
            classes.append(current)
    return tuple(classes) if classes and classes[-1] is subject else (subject,)


def document_node_identity(subject: type[object]) -> str | None:
    """Return the dotted lexical identity below the nearest canonical root."""

    if not isinstance(subject, type):
        return None
    chain = _qualified_class_chain(subject)
    start = 0
    for index, candidate in enumerate(chain):
        records = information_of(candidate)
        if any(record.type is CanonicalTitle for record in records):
            start = index + 1
    components = [candidate.__name__ for candidate in chain[start:]]
    return ".".join(components) if components else None


def canonical_document_root(subject: type[object]) -> type[object] | None:
    """Return the nearest canonical document root containing ``subject``."""

    if not isinstance(subject, type):
        return None
    root: type[object] | None = None
    for candidate in _qualified_class_chain(subject):
        if any(record.type is CanonicalTitle for record in information_of(candidate)):
            root = candidate
    return root


def _reference_class_targets(value: object):
    if isinstance(value, type):
        yield value
        return
    if isinstance(value, (tuple, list, set)):
        for item in value:
            yield from _reference_class_targets(item)


def merge_target_reference_names(target: object) -> tuple[str, ...]:
    """Return shortest-to-longest Python reference suffixes for a class target."""

    if not isinstance(target, type):
        return ()
    module = getattr(target, "__module__", "")
    qualname = getattr(target, "__qualname__", "")
    if not qualname or "<locals>" in qualname:
        return ()
    parts = [part for part in module.split(".") if part]
    parts.extend(part for part in qualname.split(".") if part)
    return tuple(".".join(parts[index:]) for index in range(len(parts) - 1, -1, -1))


@dataclass(frozen=True, slots=True)
class _FieldReference:
    """Reference target for one concrete field binding on a document node."""

    binding_name: str


def _field_values_for_reference(item, target: object) -> list[FieldValue]:
    if not isinstance(target, _FieldReference):
        return []
    return [
        value
        for value in item.values(DocumentField)
        if isinstance(value, FieldValue) and value.binding_name == target.binding_name
    ]


def _field_references_for_merge_target(item, target: object) -> tuple[_FieldReference, ...]:
    """Resolve a field merge target to concrete binding identities on this node."""

    if isinstance(target, _FieldReference):
        return (target,) if _field_values_for_reference(item, target) else ()
    if isinstance(target, _FieldBinding):
        if target.binding_name is None:
            return ()
        reference = _FieldReference(target.binding_name)
        return (reference,) if _field_values_for_reference(item, reference) else ()
    if isinstance(target, FieldWriter):
        names: list[str] = []
        for value in item.values(DocumentField):
            if not isinstance(value, FieldValue) or value.schema is not target.schema:
                continue
            if value.binding_name not in names:
                names.append(value.binding_name)
        return tuple(_FieldReference(name) for name in names)
    return ()


def _reference_target_key(target: object) -> tuple[object, ...]:
    if isinstance(target, _FieldReference):
        return ("field", target.binding_name)
    if isinstance(target, str):
        return ("literal", target)
    return ("object", id(target))


def _add_reference_claim(claims: dict[str, list[object]], name: str, target: object) -> None:
    targets = claims.setdefault(name, [])
    key = _reference_target_key(target)
    if all(_reference_target_key(candidate) != key for candidate in targets):
        targets.append(target)


def template_reference_bindings(item) -> tuple[dict[str, object], dict[str, tuple[object, ...]]]:
    """Resolve one node-local template namespace.

    Field bindings participate automatically under their Python ``@=`` left-hand
    name. ``merge`` contributes explicit aliases or Python-identity suffixes for
    class targets. Name collisions are retained and become errors only when an
    ambiguous reference is actually used by template-bearing content.
    """

    claims: dict[str, list[object]] = {}

    for binding_name in _group_fields(item):
        _add_reference_claim(claims, binding_name, _FieldReference(binding_name))

    for binding in item.values(MergeBinding):
        if not isinstance(binding, tuple) or len(binding) != 2:
            continue
        name, target = binding
        if isinstance(name, str):
            field_targets = _field_references_for_merge_target(item, target)
            if field_targets:
                for field_target in field_targets:
                    _add_reference_claim(claims, name, field_target)
            else:
                _add_reference_claim(claims, name, target)
            continue
        if name is not None:
            continue
        for reference in merge_target_reference_names(target):
            _add_reference_claim(claims, reference, target)

    resolved: dict[str, object] = {}
    ambiguous: dict[str, tuple[object, ...]] = {}
    for reference, targets in claims.items():
        if len(targets) == 1:
            resolved[reference] = targets[0]
        elif len(targets) > 1:
            ambiguous[reference] = tuple(targets)
    return resolved, ambiguous



def _group_fields(item) -> dict[str, list[FieldValue]]:
    grouped: dict[str, list[FieldValue]] = {}
    for value in item.values(DocumentField):
        if isinstance(value, FieldValue):
            grouped.setdefault(value.binding_name, []).append(value)
    return grouped

def _prose_templates(item) -> tuple[str, ...]:
    texts: list[str] = []
    for values in _group_fields(item).values():
        for entry in values:
            if entry.presentation is FieldPresentation.PROSE and isinstance(entry.value, str):
                texts.append(entry.value)
    return tuple(texts)


def _template_texts(item) -> tuple[str, ...]:
    texts = [value for value in item.values(CanonicalContent) if isinstance(value, str)]
    texts.extend(value for value in item.values(Title) if isinstance(value, str))
    texts.extend(_prose_templates(item))
    return tuple(texts)


def _reference_alternatives(
    bindings: dict[str, object], target: object
) -> tuple[str, ...]:
    key = _reference_target_key(target)
    return tuple(
        name
        for name, candidate in bindings.items()
        if _reference_target_key(candidate) == key
    )


def _validate_local_references(item):
    from ._vocabulary import vocabulary_term_name

    raw = item.values(MergeBinding)

    for binding in raw:
        if not isinstance(binding, tuple) or len(binding) != 2:
            yield Diagnostic(
                "merge bindings require an implicit class target or a (name, target) pair",
                code="document.merge.shape",
                subject=item.subject,
            )
            continue
        name, target = binding

        if name is None:
            references = merge_target_reference_names(target)
            if not references:
                yield Diagnostic(
                    "implicit merge targets require a stable Python class identity",
                    code="document.merge.name",
                    subject=item.subject,
                )
                continue
            label = references[0]
        elif isinstance(name, str) and name.isidentifier():
            label = name
        else:
            yield Diagnostic(
                "explicit merge names must be Python identifiers",
                code="document.merge.name",
                subject=item.subject,
            )
            continue

        if isinstance(target, (FieldWriter, _FieldBinding)):
            if not _field_references_for_merge_target(item, target):
                yield Diagnostic(
                    f"merge target {label!r} refers to a field not written on this document node",
                    code="document.merge.field.unwritten",
                    subject=item.subject,
                )
            continue
        if isinstance(target, str):
            continue
        if vocabulary_term_name(target) is not None:
            continue
        yield Diagnostic(
            f"merge target {label!r} has unsupported type {type(target).__name__}",
            code="document.merge.target.unsupported",
            subject=item.subject,
        )

    bindings, ambiguous = template_reference_bindings(item)
    if not bindings and not ambiguous:
        return

    for text in _template_texts(item):
        for key in placeholder_keys(text):
            targets = ambiguous.get(key)
            if not targets:
                continue
            alternatives: list[str] = []
            for target in targets:
                names = _reference_alternatives(bindings, target)
                if names:
                    alternatives.append(min(names, key=len))
                    continue
                if isinstance(target, _FieldReference):
                    alternatives.append(
                        f"explicit merge alias for field {target.binding_name!r}"
                    )
                    continue
                python_names = merge_target_reference_names(target)
                alternatives.append(
                    python_names[-1] if python_names else repr(target)
                )
            yield Diagnostic(
                f"local template reference {key!r} is ambiguous; use one of: "
                + ", ".join(repr(value) for value in alternatives),
                code="document.reference.ambiguous",
                subject=item.subject,
            )

    local_names = set(bindings) | set(ambiguous)
    for info_type, code, label in (
        (CanonicalTitle, "document.reference.title", "canonical title"),
        (CanonicalSummary, "document.reference.summary", "canonical summary"),
    ):
        for text in item.values(info_type):
            if not isinstance(text, str):
                continue
            for key in placeholder_keys(text):
                if key in local_names:
                    yield Diagnostic(
                        f"local template reference {key!r} is not allowed in {label}",
                        code=code,
                        subject=item.subject,
                    )

    # Only prose fields can recursively expand local references. Build a graph
    # over the unified local namespace and reject cycles.
    graph: dict[str, set[str]] = {name: set() for name in bindings}
    for name, target in bindings.items():
        values = _field_values_for_reference(item, target)
        if not values or values[0].presentation is not FieldPresentation.PROSE:
            continue
        for field_value in values:
            if not isinstance(field_value.value, str):
                continue
            for key in placeholder_keys(field_value.value):
                if key in bindings:
                    graph[name].add(key)

    state: dict[str, int] = {}
    stack: list[str] = []
    reported: set[tuple[str, ...]] = set()

    def visit(name: str):
        state[name] = 1
        stack.append(name)
        for target in graph[name]:
            if state.get(target, 0) == 0:
                yield from visit(target)
            elif state.get(target) == 1:
                try:
                    index = stack.index(target)
                except ValueError:  # pragma: no cover
                    index = 0
                cycle = tuple(stack[index:] + [target])
                if cycle not in reported:
                    reported.add(cycle)
                    yield Diagnostic(
                        "local reference cycle: " + " -> ".join(cycle),
                        code="document.reference.cycle",
                        subject=item.subject,
                    )
        stack.pop()
        state[name] = 2

    for name in graph:
        if state.get(name, 0) == 0:
            yield from visit(name)



def _merge_policy_for_subject(subject: object) -> MergePolicy | None:
    root = canonical_document_root(subject) if isinstance(subject, type) else None
    if root is None:
        return None
    values = tuple(
        record.value
        for record in information_of(root)
        if record.type is CanonicalMergePolicy
    )
    if len(values) == 1 and isinstance(values[0], MergePolicy):
        return values[0]
    return None


def _validate_merge_policy(item):
    policy = _merge_policy_for_subject(item.subject)
    if policy is None or policy.allows_local:
        return

    # ``merge_policy`` constrains explicit ``merge @= ...`` declarations, not
    # references to fields written directly on the same document node.  Direct
    # field bindings are intrinsic node data and remain available to templates
    # under every policy.
    if item.values(MergeBinding):
        yield Diagnostic(
            f'canonical document merge_policy="{policy.value}" forbids local merge declarations',
            code="document.merge.policy.local",
            subject=item.subject,
        )



def _validate_field_values(current):
    fields = current.values(DocumentField)
    if not fields:
        return

    by_binding: dict[str, list[FieldValue]] = {}
    schemas_by_display_name: dict[str, set[int]] = {}
    schemas_by_binding: dict[str, set[int]] = {}
    presentations_by_binding: dict[str, set[FieldPresentation]] = {}

    for field_value in fields:
        if not isinstance(field_value, FieldValue):
            continue
        schema = field_value.schema
        by_binding.setdefault(field_value.binding_name, []).append(field_value)
        schemas_by_display_name.setdefault(schema.name, set()).add(id(schema))
        schemas_by_binding.setdefault(field_value.binding_name, set()).add(id(schema))
        presentations_by_binding.setdefault(field_value.binding_name, set()).add(
            field_value.presentation
        )

        if not schema.accepts(field_value.value):
            yield Diagnostic(
                f"field {schema.name!r} does not accept value of type "
                f"{type(field_value.value).__name__}",
                code="document.field.value_type",
                subject=current.subject,
            )
        if field_value.presentation is FieldPresentation.TABLE:
            row = field_value.value
            if isinstance(row, (tuple, list)) and len(row) != len(field_value.columns):
                yield Diagnostic(
                    f"table field {schema.name!r} requires {len(field_value.columns)} "
                    f"cells per row, but {len(row)} are present",
                    code="document.field.table.row_length",
                    subject=current.subject,
                )

        if field_value.presentation is FieldPresentation.REFERENCE:
            for target in _reference_class_targets(field_value.value):
                root = canonical_document_root(target)
                if root is None or target is root:
                    continue
                policies = tuple(
                    record.value
                    for record in information_of(root)
                    if record.type is CanonicalHeadingPolicy
                )
                if len(policies) == 1 and policies[0] is not HeadingPolicy.IDENTITY:
                    yield Diagnostic(
                        "nested canonical document nodes used as semantic reference "
                        "targets require heading=\"identity\" on their canonical root",
                        code="document.reference.target.heading",
                        subject=current.subject,
                    )

    for name, definitions in schemas_by_display_name.items():
        if len(definitions) > 1:
            yield Diagnostic(
                f"field display name {name!r} is declared by more than one field definition on this node",
                code="document.field.definition.duplicate",
                subject=current.subject,
            )

    for name, definitions in schemas_by_binding.items():
        if len(definitions) > 1 or len(presentations_by_binding.get(name, ())) > 1:
            yield Diagnostic(
                f"field binding {name!r} is written by more than one field definition on this node",
                code="document.field.binding.duplicate",
                subject=current.subject,
            )

    for values in by_binding.values():
        if not values:
            continue
        schema = values[0].schema
        if schema.cardinality is Cardinality.ONE and len(values) > 1:
            yield Diagnostic(
                f"field {schema.name!r} allows one value, but {len(values)} values are present",
                code="document.field.cardinality",
                subject=current.subject,
            )


def _validate_container(view):
    roots = _document_roots(view)
    if not roots:
        yield Diagnostic(
            "canonical document descriptions require at least one @canonical_source(...) root",
            code="document.required",
        )
        return

    filenames: dict[str, object] = {}
    orders: dict[int, object] = {}

    for root in roots:
        filenames_values = root.values(CanonicalFilename)
        if len(filenames_values) == 1 and filename_value_error(
            filenames_values[0], label="canonical filename"
        ) is None:
            key = filenames_values[0].casefold()
            previous = filenames.get(key)
            if previous is not None:
                yield Diagnostic(
                    f"canonical filename {filenames_values[0]!r} is already used",
                    code="document.filename.duplicate",
                    subject=root.subject,
                )
            else:
                filenames[key] = root.subject

        order_values = root.values(CanonicalOrder)
        if len(order_values) == 1:
            order = order_values[0]
            if isinstance(order, int) and not isinstance(order, bool) and order >= 0:
                previous = orders.get(order)
                if previous is not None:
                    yield Diagnostic(
                        f"canonical order {order} is already used",
                        code="document.order.duplicate",
                        subject=root.subject,
                    )
                else:
                    orders[order] = root.subject

    allowed = {
        id(item.subject)
        for root in roots
        for item in _document_members(view, root)
    }
    for candidate in view.entities:
        has_node_data = (
            candidate.values(DocumentField)
            or candidate.values(MergeBinding)
            or candidate.values(Title)
            or candidate.values(CanonicalSummary)
        )
        if has_node_data and id(candidate.subject) not in allowed:
            yield Diagnostic(
                "document metadata, fields, merges, and node titles must belong to a canonical document root",
                code="document.node.parent",
                subject=candidate.subject,
            )


@validator(focus=StructuralKind.MODULE)
def document_module(view):
    if isinstance(view.focused.node.parent, ModuleType):
        return
    yield from _validate_container(view)


@validator(focus=StructuralKind.PACKAGE)
def document_package(view):
    if isinstance(view.focused.node.parent, ModuleType):
        return
    yield from _validate_container(view)


@validator(focus=StructuralKind.ENTITY)
def document_entity(view):
    current = view.focused

    if current.has(CanonicalTitle):
        if not isinstance(current.node.parent, ModuleType):
            yield Diagnostic(
                "canonical document roots must be top-level classes in a module",
                code="document.top_level",
                subject=current.subject,
            )
        if current.values(Title):
            yield Diagnostic(
                "root title belongs in @canonical_source(...), not title @= ...",
                code="document.root_title",
                subject=current.subject,
            )
        for info_type, code, message in (
            (CanonicalTitle, "document.title.required", "canonical document roots require exactly one title"),
            (CanonicalContent, "document.content.required", "canonical document roots require exactly one content template"),
            (CanonicalFilename, "document.filename.required", "canonical document roots require exactly one filename"),
            (CanonicalDocumentPath, "document.path.required", "canonical document roots require exactly one logical document path"),
            (CanonicalMergePolicy, "document.merge_policy.required", "canonical document roots require exactly one merge policy"),
            (CanonicalUnreferencedFields, "document.fields.policy.required", "canonical document roots require exactly one unreferenced-field policy"),
            (CanonicalHeadingPolicy, "document.heading.required", "canonical document roots require exactly one heading policy"),
            (CanonicalSource, "document.canonical_source.required", "canonical document roots require exactly one canonical source"),
        ):
            if len(current.values(info_type)) != 1:
                yield Diagnostic(message, code=code, subject=current.subject)

        for filename in current.values(CanonicalFilename):
            error = filename_value_error(filename, label="canonical filename")
            if error is not None:
                yield Diagnostic(error, code="document.filename.value", subject=current.subject)

        if len(current.values(CanonicalSummary)) > 1:
            yield Diagnostic(
                "canonical document roots allow at most one summary",
                code="document.summary.cardinality",
                subject=current.subject,
            )

        orders = current.values(CanonicalOrder)
        if len(orders) > 1:
            yield Diagnostic(
                "canonical document roots allow at most one order",
                code="document.order.cardinality",
                subject=current.subject,
            )
        for order in orders:
            if isinstance(order, bool) or not isinstance(order, int) or order < 0:
                yield Diagnostic(
                    "canonical order must be a non-negative integer",
                    code="document.order.value",
                    subject=current.subject,
                )

    elif current.values(CanonicalContent):
        if len(current.values(CanonicalContent)) != 1:
            yield Diagnostic(
                "document nodes require exactly one content template",
                code="document.node.content.required",
                subject=current.subject,
            )
        if len(current.values(Title)) > 1:
            yield Diagnostic(
                "document nodes allow at most one title",
                code="document.node.title.cardinality",
                subject=current.subject,
            )
        if any(
            current.values(info_type)
            for info_type in (
                CanonicalSource,
                CanonicalSummary,
                CanonicalTitle,
                CanonicalFilename,
                CanonicalDocumentPath,
                CanonicalOrder,
                CanonicalMergePolicy,
                CanonicalUnreferencedFields,
                CanonicalHeadingPolicy,
            )
        ):
            yield Diagnostic(
                "canonical document metadata belongs on document roots",
                code="document.metadata.root_only",
                subject=current.subject,
            )

    elif (
        current.values(DocumentField)
        or current.values(MergeBinding)
        or current.values(Title)
        or current.values(CanonicalSummary)
    ):
        yield Diagnostic(
            "document metadata, fields, merges, and node titles require a canonical document node",
            code="document.node.required",
            subject=current.subject,
        )

    if current.has(CanonicalTitle) or current.values(CanonicalContent):
        yield from _validate_local_references(current)
        yield from _validate_merge_policy(current)

    yield from _validate_field_values(current)


_entity = StructureSelector(kind=StructuralKind.ENTITY)


document = Shikumi(
    structure=PackageTreeStructure(),
    information_types=[
        Title,
        DocumentField,
        MergeBinding,
        CanonicalSource,
        CanonicalSummary,
        CanonicalTitle,
        CanonicalContent,
        CanonicalDocumentPath,
        CanonicalFilename,
        CanonicalOrder,
        CanonicalMergePolicy,
        CanonicalUnreferencedFields,
        CanonicalHeadingPolicy,
    ],
    descriptor_rules=[
        DescriptorUseRule(descriptor=canonical_source, allowed=_entity, name="canonical_source"),
        DescriptorUseRule(descriptor=summary, allowed=_entity, name="summary"),
        DescriptorUseRule(descriptor=merge, allowed=_entity, name="merge"),
        DescriptorUseRule(descriptor=title, allowed=_entity, name="title"),
    ],
    validators=[
        information_type_rule(Title),
        information_type_rule(DocumentField),
        information_type_rule(MergeBinding),
        information_type_rule(CanonicalSource),
        information_type_rule(CanonicalSummary),
        information_type_rule(CanonicalTitle),
        information_type_rule(CanonicalContent),
        information_type_rule(CanonicalDocumentPath),
        information_type_rule(CanonicalFilename),
        information_type_rule(CanonicalOrder),
        information_type_rule(CanonicalMergePolicy),
        information_type_rule(CanonicalUnreferencedFields),
        information_type_rule(CanonicalHeadingPolicy),
        document_module,
        document_package,
        document_entity,
    ],
)
