# Realizers

Public realization APIs that transform validated semantic views into Markdown or Python reference modules.

## shikumi_devdoc.realizers

Realization APIs grouped by purpose.

name: shikumi_devdoc.realizers

kind: Namespace

related: [DIST_008](../specification/distribution.md#dist_008-namespaced-realizer-surface)

### shikumi_devdoc.realizers.common

Values shared across realizers.

name: shikumi_devdoc.realizers.common

kind: Namespace

#### shikumi_devdoc.realizers.common.MarkdownDocument

Value containing a filename and content for one Markdown artifact.

name: shikumi_devdoc.realizers.common.MarkdownDocument

kind: Type

### shikumi_devdoc.realizers.document

Canonical-document realization API.

name: shikumi_devdoc.realizers.document

kind: Namespace

#### shikumi_devdoc.realizers.document.MarkdownRealizer

Realizer that converts canonical-document roots in a validated `SemanticView` into `MarkdownDocument` artifacts.

name: shikumi_devdoc.realizers.document.MarkdownRealizer

kind: Type

input: view [SemanticView]: semantic view validated by the document system.

output: output [tuple[MarkdownDocument, ...]]: Markdown artifacts for each `@canonical_source(..., filename=...)` root.

### shikumi_devdoc.realizers.index

Canonical-document collection index realization API.

name: shikumi_devdoc.realizers.index

kind: Namespace

#### shikumi_devdoc.realizers.index.IndexMarkdownRealizer

Realizer that produces a Markdown index from canonical-document metadata in a package-level `SemanticView`.

name: shikumi_devdoc.realizers.index.IndexMarkdownRealizer

kind: Type

input: view [SemanticView]: semantic view obtained by validating a package with the document system.

output: output [MarkdownDocument]: index listing canonical-document links and summaries derived from title, filename, and `@summary(...)` metadata.

detail: `IndexMarkdownRealizer` requires a package focus and one `@summary(...)` per canonical document. It does not generate document bodies or expose canonical-source paths in the index.

### shikumi_devdoc.realizers.vocabulary

Vocabulary realization API.

name: shikumi_devdoc.realizers.vocabulary

kind: Namespace

#### shikumi_devdoc.realizers.vocabulary.GlossaryMarkdownRealizer

Realize Markdown glossary output for Vocabulary terms marked for publication.

name: shikumi_devdoc.realizers.vocabulary.GlossaryMarkdownRealizer

kind: Type

### shikumi_devdoc.realizers.translation

Realization APIs and values for the translation boundary.

name: shikumi_devdoc.realizers.translation

kind: Namespace

#### shikumi_devdoc.realizers.translation.PreserveSpellingTerm

Value describing a Vocabulary term whose spelling should survive translation unchanged.

name: shikumi_devdoc.realizers.translation.PreserveSpellingTerm

kind: Type

#### shikumi_devdoc.realizers.translation.TranslationManifest

Value carrying Vocabulary policy across the translation boundary.

name: shikumi_devdoc.realizers.translation.TranslationManifest

kind: Type

#### shikumi_devdoc.realizers.translation.translation_manifest

Collect a `TranslationManifest` and diagnostics from a semantic view.

name: shikumi_devdoc.realizers.translation.translation_manifest

kind: Operation

#### shikumi_devdoc.realizers.translation.SourceRealizer

Wrapper around a Markdown realizer that attaches machine-readable metadata for the translation boundary.

name: shikumi_devdoc.realizers.translation.SourceRealizer

kind: Type

detail: Scope: document prose is not translated; only semantic information needed by a later translation step is carried forward.
