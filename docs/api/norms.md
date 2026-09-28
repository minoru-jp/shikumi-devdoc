# Regulations and descriptors

Public authoring DSL for canonical sources.

## shikumi_devdoc.norms

Document-authoring APIs grouped by semantic area.

name: shikumi_devdoc.norms

kind: Namespace

related: [DIST_007](../specification/distribution.md#dist_007-namespaced-norms-authoring-surface)

### shikumi_devdoc.norms.common

Descriptors and policies shared across canonical-source kinds.

name: shikumi_devdoc.norms.common

kind: Namespace

#### shikumi_devdoc.norms.common.APPEND

Policy value that appends fields not referenced by a body template to the end of their document node.

name: shikumi_devdoc.norms.common.APPEND

kind: Value

#### shikumi_devdoc.norms.common.IGNORE

Policy value that keeps fields not referenced by templates out of the canonical document while retaining them in canonical source semantic information.

name: shikumi_devdoc.norms.common.IGNORE

kind: Value

#### shikumi_devdoc.norms.common.canonical_source

Decorator that marks a canonical source unit. For canonical documents it declares the root title, filename, `heading="title"|"identity"` nested-heading policy, optional order, `merge_policy="all"|"local"|"external"|"forbidden"`, and the unreferenced-field policy. The legacy `placeholders` parameter is deprecated in 0.3.2 and scheduled for removal in 1.0.0.

name: shikumi_devdoc.norms.common.canonical_source

kind: Operation

related: [CORE_001](../specification/core.md#core_001-canonical-source), [CORE_007](../specification/core.md#core_007-canonical-source-provenance)

#### shikumi_devdoc.norms.common.summary

Decorator factory that attaches concise summary metadata to a canonical source/document for collection-level overviews such as generated indexes.

name: shikumi_devdoc.norms.common.summary

kind: Operation

#### shikumi_devdoc.norms.common.merge

Writer that adds references to a document node's local template namespace. A supported class target can be declared with `merge @= target` and referenced by the shortest unambiguous suffix of its Python identity. `merge @= ("name", target)` remains available for explicit aliases, literal strings, and fields written on the same node. Canonical Vocabulary term classes can be used directly as targets. Field `@=` bindings participate in the same local namespace without requiring `merge`.

name: shikumi_devdoc.norms.common.merge

kind: Value

### shikumi_devdoc.norms.document

Generic canonical-document authoring API. Writers returned by the field factories automatically expose their `@=` left-hand binding names as local template references on the same document node.

name: shikumi_devdoc.norms.document

kind: Namespace

#### shikumi_devdoc.norms.document.title

Assignment-only writer for a nested document node's human-readable title. The title can resolve same-node local merges and realization context, and is realized either as the visible heading or as human-readable metadata according to the canonical document's heading policy.

name: shikumi_devdoc.norms.document.title

kind: Value

#### shikumi_devdoc.norms.document.field

Create a literal scalar field writer. Canonical display name and Python binding name are independent; the `@=` left-hand binding name becomes a local template reference on the same node.

name: shikumi_devdoc.norms.document.field

kind: Operation

#### shikumi_devdoc.norms.document.list_field

Create a repeatable literal field writer that realizes each `@=` value as a Markdown bullet-list item.

name: shikumi_devdoc.norms.document.list_field

kind: Operation

#### shikumi_devdoc.norms.document.test_target_field

Create a field writer that separates literal text for direct inspection by ordinary tests. It does not add Markdown fences or language info strings; presentation belongs to the surrounding template.

name: shikumi_devdoc.norms.document.test_target_field

kind: Operation

#### shikumi_devdoc.norms.document.table_field

Create a repeatable literal field writer whose rows are realized as a Markdown table with the declared columns.

name: shikumi_devdoc.norms.document.table_field

kind: Operation

#### shikumi_devdoc.norms.document.prose_field

Create a named Markdown prose template fragment. It follows the same local-reference, external-placeholder, and escape rules as document-node docstrings.

name: shikumi_devdoc.norms.document.prose_field

kind: Operation

#### shikumi_devdoc.norms.document.system

Shikumi system that validates canonical-document roots, nested document nodes, fields, and local template references.

name: shikumi_devdoc.norms.document.system

kind: Value

related: [DOC_001](../specification/document.md#doc_001-nested-classes-define-heading-hierarchy), [DOC_002](../specification/document.md#doc_002-docstrings-are-templates)

#### shikumi_devdoc.norms.document.reference_field

Creates a field writer that retains Python object relationships as semantic references and realizes resolvable canonical document nodes as logical Markdown links.

name: shikumi_devdoc.norms.document.reference_field

kind: Operation

### shikumi_devdoc.norms.vocabulary

API for applying Vocabulary semantics to an ordinary canonical source.

name: shikumi_devdoc.norms.vocabulary

kind: Namespace

#### shikumi_devdoc.norms.vocabulary.vocabulary

Marker decorator that interprets a `@canonical_source(...)` root as a Vocabulary. Each direct child's docstring is normalized with `inspect.cleandoc()`-equivalent behavior, then its leading `{{term name}}` declaration defines the term name and the remaining docstring becomes the definition.

name: shikumi_devdoc.norms.vocabulary.vocabulary

kind: Operation

#### shikumi_devdoc.norms.vocabulary.preserve_spelling

Writer used with `@=` to declare that a term's spelling should survive translation unchanged.

name: shikumi_devdoc.norms.vocabulary.preserve_spelling

kind: Value

#### shikumi_devdoc.norms.vocabulary.glossary

Writer used with `@=` to override a term's public-Glossary selection. Terms are public by default; assign `False` to exclude one.

name: shikumi_devdoc.norms.vocabulary.glossary

kind: Value

#### shikumi_devdoc.norms.vocabulary.alias

Writer used with `@=` to add alternate names for a term.

name: shikumi_devdoc.norms.vocabulary.alias

kind: Value

#### shikumi_devdoc.norms.vocabulary.deprecated

Writer used with `@=` to mark a term as deprecated.

name: shikumi_devdoc.norms.vocabulary.deprecated

kind: Value

#### shikumi_devdoc.norms.vocabulary.replacement

Writer used with `@=` to record the replacement canonical name for a deprecated term.

name: shikumi_devdoc.norms.vocabulary.replacement

kind: Value

#### shikumi_devdoc.norms.vocabulary.system

Shikumi system that validates Vocabulary source.

name: shikumi_devdoc.norms.vocabulary.system

kind: Value
