# Canonical document structure

Rules for canonical-document node hierarchy, templates, and local references.

## DOC_001 Nested classes define heading hierarchy

Every class lexically nested under an `@canonical_source(...)` root must be interpreted as a child document node, and nesting must map directly to canonical Markdown heading hierarchy.

level: MUST

## DOC_002 Docstrings are templates

The docstring of the canonical root and each child document node must be normalized with behavior equivalent to `inspect.cleandoc()` before it is treated as that node's body template. Common indentation caused by Python source layout must not become canonical content, while relative indentation within the body must be preserved.

level: MUST

## DOC_003 Raw Markdown headings

Raw Markdown headings inside body templates must not be used as a substitute for semantic document hierarchy. Document structure is expressed with nested classes.

level: MUST NOT

## DOC_004 Parallel string node identities

Document nodes must not define string anchor identities in parallel with their Python entities. Semantic references in canonical source should use Python entities whenever possible.

level: MUST NOT

## DOC_005 External values

Values that may change at realization time, such as the current release, should be read from realization context rather than frozen into canonical source. Context must not be used to store historical facts or normative content.

level: SHOULD

## DOC_006 Relations are ordinary fields

Relationship information may be recorded through ordinary field vocabulary. The standard `related` field is a convenience field that retains already-resolved Python class objects as semantic references; the generic document core does not assign direction or meaning to those relationships. Whether and where the field is rendered must follow the same local-reference and unreferenced-field policies as any other field.

level: MAY

related: [SPEC_008](specification.md#spec_008)

## DOC_007 Unified local references

When a field writer is used as `name @= value`, the left-hand binding name `name` must automatically become a local reference on that document node. `merge @= target` must add references for a class target from its Python identity; canonical Vocabulary term classes are supported directly. `merge @= ("name", target)` remains available for explicit aliases, literal strings, and aliases to fields written on the same node. Within a template, `{{name}}` must resolve a unique same-node local reference first and otherwise be treated as an external placeholder.

level: MUST

## DOC_008 Local-reference scope and validation

Local references must apply only to the same document node and must not be inherited implicitly by parent nodes, child nodes, or other canonical documents. Field bindings, implicit class-target names, and explicit merge aliases may collide without making registration itself invalid; an error occurs only when template-bearing content actually uses an ambiguous name. A class target can be qualified with the Vocabulary/container name and, if necessary, module path until it is unique. A field can be given an explicit merge alias when another name is needed. Targets referring to unwritten fields, unsupported targets, and local-reference cycles through `prose_field` must be validation errors.

level: MUST

## DOC_009 Template escape

Template-bearing content must allow `\{{...}}` to escape a placeholder marker as literal text. `${{...}}` must be preserved literally as host-language syntax.

level: MUST

## DOC_010 Literal fields stay literal

Values of `field`, `list_field`, `table_field`, and `test_target_field` must be treated as literal content. `{{...}}` inside those values must not be interpreted as placeholders or merges.

level: MUST

## DOC_011 Prose fields are template fragments

`prose_field` must be treated as a named body-template fragment following the same template rules as a docstring, including external placeholders and same-node local references.

level: MUST


## DOC_012 Unified title information

A nested document node must record at most one human-readable title with `title @= "..."`. `@title(...)` must not be provided as an alternative title syntax. Title text uses the same node-local template namespace as docstrings and `prose_field`; after resolving same-node `merge` references and external placeholders, the result must be one non-empty line.

level: MUST
