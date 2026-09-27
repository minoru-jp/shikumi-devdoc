# Field presentations

Rules for generic Markdown structures available to author-defined fields.

## FIELD_001

A field factory may name authoring intent, but generic realizer behavior must follow only the literal/template/reference and document-structure contract explicitly declared by that factory. It must not infer additional domain meaning or presentation from field names or values.

title: Explicit field behavior

level: MUST

## FIELD_002

`field()` must retain one or more literal values as compact inline content. When an unreferenced field is appended automatically, its default form is `name: value`.

title: Inline field

level: MUST

## FIELD_003

`list_field()` must realize each `@=` value as a Markdown bullet-list item under the same field.

title: List field

level: MUST

## FIELD_004

`test_target_field()` must retain string fragments as literal test targets intended for direct inspection by ordinary tests. The realizer must not add a fenced code block, language info string, or other Markdown presentation implicitly; when referenced from a template it inserts only normalized literal text.

title: Test target field

level: MUST

## FIELD_005

A `test_target_field()` value denotes author intent to expose a fragment to ordinary tests, but must not imply that a corresponding test exists or has passed.

title: Test coverage is not implied

level: MUST NOT

## FIELD_006

When a `test_target_field()` value is documented as code, configuration, a command, expected output, or similar content, fences and language markers should be written in the docstring or `prose_field` template, and ordinary tests should validate the field value itself.

title: Test-target presentation and verification

level: SHOULD

## FIELD_007

`table_field()` must realize each `@=` row as one Markdown table row using the declared columns, and row-width mismatch must be a validation error.

title: Table field

level: MUST

## FIELD_008

`prose_field()` must hold a named Markdown prose template fragment and must follow the same local-reference, external-placeholder, and escape rules as docstring templates.

title: Prose field

level: MUST

## FIELD_009

The distinction between literal fields and `prose_field` must determine only whether the value is interpreted as a template or retained as literal content, not the domain meaning of that value.

title: Template-bearing versus literal fields

level: MUST

## FIELD_010

`reference_field()` must retain Python object relationships as semantic references instead of flattening them to literal text. When the Markdown realizer can resolve the source and target canonical document logical paths together with the target's rendered heading, it must derive a deterministic relative logical Markdown link from that metadata. Values that cannot be resolved this way must fall back to the same stable representation used for literal fields.

title: Reference field

level: MUST
