# Structured fields

Rules for author-defined fields and self-contained canonical documents.

## SPEC_001

Every class lexically nested under a canonical root is a document node. Its identity must be derived from the Python class name and class nesting; no per-node decorator is required.

title: Class-derived document-node identity

level: MUST

## SPEC_002

The canonical display name declared by `field(name, value_type, ...)`, the Python variable holding the writer, and the left-hand binding name used with `@=` must be independent.

title: Author-defined field names

level: MUST

## SPEC_003

Each canonical document must declare its Markdown filename through `@canonical_source(..., filename=...)` and must be independently validatable and realizable.

title: Self-contained document filename

level: MUST

## SPEC_004

`@canonical_source(..., order=...)` may be supplied only when multiple documents need stable ordering.

title: Optional document order

level: MAY

## SPEC_005

Document-node nesting must be interpreted as canonical Markdown heading nesting. Depth that Markdown cannot represent must be rejected by realization checks.

title: Node nesting is heading nesting

level: MUST

condition: When realizing Markdown.

## SPEC_006

Even when unreferenced fields are emitted automatically, a field name alone must never promote a field into a Markdown heading. Field presentation follows the document structure declared by its field factory.

title: Fields are not headings

level: MUST

## SPEC_007

Domain vocabularies such as Specification, API Reference, and ADR must be definable by consumers or separate libraries as sets of field writers such as `field()`.

title: External domain field vocabularies

level: MUST

## SPEC_008

When a Python class is used as a field value, that entity must already be resolved when the expression is evaluated. The foundation must not add string-ID, forward-reference, or symbolic-reference resolution.

title: Direct Python references

level: MUST

## SPEC_009

Individual canonical-document realization and collection-index realization must be independent operations. The standard document realizer must not generate `INDEX.md` implicitly; the index realizer must generate only an index from the canonical-source collection in an explicitly selected package.

title: Separate document and index realization

level: MUST

## SPEC_010

The realizer must not restructure the document-node hierarchy from domain semantics. It must map the author's class hierarchy directly to Markdown heading hierarchy.

title: Preserve author hierarchy

level: MUST

## SPEC_011

Multiple canonical documents must be treated as independent `@canonical_source(...)` roots without depending on a shared collection-root entity.

title: No collection-root dependency

level: MUST
