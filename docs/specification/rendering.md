# Rendering

Rules for Markdown realization, realization context, and the canonical-document boundary.

## RENDER_001

A standard Markdown realizer must provide `check()` diagnostics for realizability before realization.

title: Realization check

level: MUST

## RENDER_002

An unknown context placeholder must be diagnosed rather than silently replaced with an empty string.

title: Unknown context reference

level: MUST

condition: When realizing a canonical document or Glossary.

## RENDER_003

A standard realizer that produces multiple files must return a collection of `MarkdownDocument` values containing filenames and bodies. Canonical-document filenames come from each root `@canonical_source(..., filename=...)` declaration.

title: Partition output

level: MUST

related: [SPEC_003](specification.md#spec_003)

## RENDER_004

When handing a canonical document to a later translation step, Vocabulary spelling-preservation policy may be embedded as machine-readable metadata through `TranslationSourceRealizer`.

title: Translation metadata

level: SHOULD

## RENDER_005

Operational comments at the beginning of generated artifacts must be explicitly supplied by the caller. A realizer must not discover project-specific wording implicitly.

title: Header comments are caller supplied

level: MUST

## RENDER_006

The standard index realizer must consume a `SemanticView` produced by validating a package with the document system, collect the `@canonical_source(...)` roots in that package tree, and generate one Markdown index. It must not generate a collection index from a module focus.

title: Package-level collection index

level: MUST

related: [SPEC_009](specification.md#spec_009), [SPEC_011](specification.md#spec_011)

## RENDER_007

The standard index realizer must require `@summary(...)` metadata on every indexed canonical document and present the document link together with that summary. It must not expose author-side implementation details such as canonical-source paths in the index body.

title: Index summary metadata

level: MUST

## RENDER_008

The standard document Markdown realizer must realize each nested document node as an ATX heading and must derive the logical fragment used by semantic references deterministically from the heading text it actually emits. With `heading="title"`, the resolved `title @= ...` value becomes the heading, falling back to the class identity when no title exists. With `heading="identity"`, the class identity is always the heading and any title is realized as human-readable metadata. The standard transformation adopts GitHub-compatible heading-slug behavior as the logical reference convention: strip surrounding whitespace, lowercase the heading, retain only Unicode alphanumeric characters, `-`, `_`, and whitespace, then replace each run of whitespace with `-`. This is not a Markdown-standard guarantee about fragments; if a downstream renderer uses different fragment rules, publication processing owns that adjustment. The realizer must not add explicit HTML anchors.

title: Heading-derived logical fragments

level: MUST

## RENDER_009

When a reference-presented value targets a canonical document node, the standard document Markdown realizer must derive the relative document path from the source and target canonical document logical paths, then combine it with the logical fragment derived from the heading text actually emitted for the target node. A fragment-only link may be used within the same document. The realizer must not inspect or infer whether the target document is generated in the same invocation, exists on the filesystem, what realization output directory is used, or whether publication preserves the same relative layout.

title: Logical reference links

level: MUST

related: [CORE_012](core.md#core_012-canonical-document-logical-path)

## RENDER_010

If a publication process changes the relative topology or filenames represented by canonical document logical paths, or uses a downstream Markdown renderer with different heading-fragment rules, any necessary link rewriting must be the responsibility of that publication process. Such publication differences must not cause canonical semantic relations to be replaced with Markdown paths or fragments in canonical source.

title: Publication layout owns link rewrites

level: MUST


## RENDER_011 Stable nested reference targets require identity headings

A canonical document root may be a semantic reference target through its filename. A nested canonical document node may be a `reference_field` target only when its containing root uses `heading="identity"`. A nested heading produced from `heading="title"` can change when its title, Vocabulary terms, or realization context changes and therefore must not be treated as a stable semantic reference target.

title: Stable nested reference targets require identity headings

level: MUST
