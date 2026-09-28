# shikumi-devdoc Changelog

## V0_3_2

version: 0.3.2

Added:

- Added `merge_policy="all" | "local" | "external" | "forbidden"` to `@canonical_source(...)`. The policy independently expresses whether template-bearing content may merge node-local references and realization-context values. `"forbidden"` supports snapshot sources that must not be recomposed from either source.

Changed:

- `merge_policy="external"` and `merge_policy="forbidden"` reject `merge @= ...` declarations even when unused, and reject local template references including field bindings. Literal field values remain literal and may still be stored.
- The project's own CHANGELOG canonical source now uses `merge_policy="forbidden"` so historical release snapshots cannot change through later local or external values.

Deprecated:

- Deprecated `@canonical_source(..., placeholders=...)`. `placeholders=True` is interpreted as `merge_policy="all"`; `placeholders=False` is interpreted as `merge_policy="local"`. Direct API use emits `DeprecationWarning`, and CLI use surfaces the warning. `placeholders` is scheduled for removal in 1.0.0.

This changelog records the versioned change history of `shikumi-devdoc`. Development milestones that were not published are explicitly identified as such.

## V0_3_1

This release clarifies the roles of the distribution artifacts and makes the sdist a complete source distribution sufficient to reconstruct and verify the release.

version: 0.3.1

Changed:

- Changed sdist file selection in `pyproject.toml` from an explicit `include` list to a policy that respects VCS ignore rules and explicitly excludes only repository-operation content. The resulting release source includes `src/`, `tests/`, `devdocs/`, `docs/`, `scripts/`, plus the root release documents and build metadata.
- Made `scripts/check_dist.py` required sdist content and updated the distribution contract so the sdist itself can be used to re-run build, archive-content, installation, CLI, `pip check`, and dogfood-rendering verification.
- Kept the wheel role unchanged: it contains the implementation, the `devdocs/` reference corpus, and the published README, Project Status, CHANGELOG, and `docs/` as package resources.

## V0_3_0

This release unifies the dedicated developer-document systems into a generic canonical-document model with author-defined field vocabularies.

version: 0.3.0

Added:

- Added `field`, `list_field`, `table_field`, `test_target_field`, `prose_field`, `reference_field`, and the shared document `system` under `shikumi_devdoc.norms.document`. Field factories define explicit literal/template/reference and document-structure behavior; the generic core does not infer additional domain meaning or presentation from field names or values.
- Added logical reference-link realization for `reference_field` and the standard `related` field. Canonical document logical paths are derived from canonical-source provenance plus declared filenames; the realizer relativizes source and target logical paths and combines that result with a fragment derived deterministically from the Markdown heading actually emitted for the target node. Fragments use a GitHub-compatible heading-slug convention without adding explicit HTML anchors, so separately rendered reference sources and targets still agree without inspecting output directories or the filesystem.
- Added `APPEND` and `IGNORE` under `shikumi_devdoc.norms.common` so each canonical document can choose whether fields not referenced by body templates are emitted automatically or retained only as source information.
- Added generic local merge declarations with `merge @= ("name", target)`. Docstrings and `prose_field` templates use the uniform `{{name}}` syntax; the standard resolver accepts strings, fields on the same node, and Vocabulary term references. Template markers can be escaped with `\{{...}}`.
- Removed `code_field` and added `test_target_field` for literal text that ordinary tests should inspect directly. Markdown fences and language info strings now belong to the surrounding template rather than the field.
- Added `shikumi_devdoc.fields.lifecycle` with `introduced`, `deprecated`, `removed`, `replacement`, and `migration`, allowing lifecycle information about APIs, specification items, and other documented subjects to live alongside the subject independently from release-centered CHANGELOG entries.
- Added `shikumi_devdoc.realizers.index.IndexMarkdownRealizer` and `render index`, allowing a canonical-source package to be indexed independently from document realization using document titles, output filenames, and `@summary(...)` metadata.
- Added `@summary(...)` as concise canonical-source/document metadata. The index realizer now emits document links and summaries instead of exposing canonical-source paths.
- Added the public `shikumi_devdoc.fields` namespace with standard field sets and related constants commonly used by Specification, API Reference, CHANGELOG, and Project Status documents. These are optional convenience APIs composed from generic field primitives and have no dedicated validator or realizer.
- Added the Authoring Guide as a canonical-document collection organized around purpose-specific patterns for README, Getting Started, Configuration Guide, CLI documentation, Specification, API Reference, CHANGELOG, Glossary / Vocabulary, Project Status, and document collections. Cross-cutting decisions are consolidated under Advanced authoring, with a separate LLM workflow.
- Added dogfooding for documentation test targets: code, configuration, commands, and similar fragments intended for verification are separated with `test_target_field` as pure literal text and checked by ordinary Python modules and pytest without evaluating documentation strings through `eval` or `exec`.

Changed:

- `@canonical_source(...)` now requires an explicit `heading="title"` or `heading="identity"` policy for canonical documents. The realizer does not infer heading presentation from the document kind.
- Changed the runtime requirement for `shikumi-devdoc 0.3.0` to `shikumi>=0.2.0`, making the post-breaking-change Shikumi 0.2.0 release the explicit compatibility baseline. No upper bound is imposed because Shikumi intends to preserve backward compatibility from 0.2.0 onward unless a concrete incompatibility is found.
- Unified nested-node human-readable titles under assignment-only `shikumi_devdoc.norms.document.title` using `title @= "..."`. Title text can resolve same-node local merges and realization context; `heading="title"` realizes the resolved title as the heading, while `heading="identity"` keeps the class identity as the heading and emits the title as human-readable metadata.
- Nested canonical document nodes used as `reference_field` targets must belong to roots with `heading="identity"`, preserving stable fragments when titles, Vocabulary terms, or context change. Document roots remain referenceable by filename regardless of heading policy.
- Renamed `@canonical` to `@canonical_source` so the public decorator name matches the canonical-source concept. Document roots carry title, filename, optional order, external-placeholder policy, and unreferenced-field policy.
- Removed the Narrative/Itemized grammar split. Every class nested under `@canonical_source(...)` is a document node, every node docstring is a body template, and the same document realizer handles README, STATUS, CHANGELOG, Specification, and API Reference.
- Document-root and document-node docstrings are normalized with `inspect.cleandoc()`-equivalent behavior before becoming semantic content. Common Python source indentation is removed while relative indentation inside the body is preserved; raw/non-raw strings and quote style are author choices rather than document semantics.
- Clarified in the Authoring Guide that `shikumi-devdoc` does not prescribe a fixed documentation set. Projects should create only the documents they need, and the purpose-specific pages are recommended compositions of the generic canonical-document model rather than mandatory document types.
- Added an authoring convention that narrative nodes may use opaque stable identities such as `SECTION_NNN`, independent of visible titles, order, and heading depth, without validator enforcement. The Specification authoring pattern also recommends using `related` as a directed semantic dependency and reconsidering the document structure when Python imports become cyclic.
- Ordinary `field`, `list_field`, `table_field`, and `test_target_field` values are literal and do not interpret placeholder-looking text. `prose_field` is template-bearing and follows the same local-reference, external-placeholder, and escape rules as docstrings.
- Clarified `placeholders=False` as a prohibition on external placeholders in template-bearing content. Node-local references and placeholder-looking text in literal fields remain usable in snapshot documents.
- Migrated the repository's Specification, API Reference, Project Status, and CHANGELOG dogfooding to the unified document model and the standard field sets under `shikumi_devdoc.fields`.
- Unified CLI document realization under `shikumi-devdoc render document`.
- Removed the Specification/API Reference `root.py` documents that duplicated collection membership. Individual documents now use `render document`, while package indexes are generated in parallel with `render index`.
- Unified `related` from two separate mechanisms into the single generic `shikumi_devdoc.fields.common.related` reference field. Its placement follows the same merge / `APPEND` / `IGNORE` policies as other fields, while visible values are realized as logical Markdown links from canonical metadata. The realizer does not inspect or infer the final publication layout or rewrite links for publication-specific relocation.
- Generalized Vocabulary authoring around ordinary `@canonical_source(...)` roots plus the `@vocabulary` semantic-profile marker. Removed `@title` / `@term` and the `VOCABULARY` / `TERM_N` naming constraints; each direct child's docstring is normalized with `inspect.cleandoc()`-equivalent behavior and must then begin with its single `{{term name}}` declaration, with the remaining docstring becoming the definition.
- Removed document-side Vocabulary attachment and `vocabulary_refs`. Canonical Vocabulary term classes are now used directly as generic `merge` targets, so term rendering, IDE navigation, and `preserve_spelling` translation metadata follow the same canonical term identity.
- Vocabulary `glossary` selection now defaults to public (`True`) when omitted. Only terms explicitly marked with `glossary @= False` are excluded from the public Glossary. The SemanticView does not receive an implicit `True`; the Glossary realizer applies the effective default.
- Added the `merge @= target` shorthand for class targets. Templates can reference the shortest unambiguous suffix of the target's Python identity. Colliding short names such as `TERM_001` across multiple Vocabularies are allowed; references can be qualified with the Vocabulary/container name and, if necessary, module path. Ambiguity is reported only when an ambiguous reference is used. Explicit `merge @= ("name", target)` aliases remain available for strings, fields, and chosen aliases.
- Field-writer `@=` bindings now enter the same node-local template namespace automatically, unifying field and `merge` name resolution. Name collisions do not fail at registration time; only an actually used ambiguous reference is rejected. Reusing one `FieldWriter` under multiple binding names now preserves each binding as a distinct reference and value group.

Fixed:

- Restored dogfooding of the dedicated Glossary projection after the Vocabulary generalization by defining the default public-term selection, restoring `render glossary` to the generation workflow, and regenerating `GLOSSARY.md` as a canonical document.

Removed:

- Removed the generic document-node `@title(...)` decorator syntax. Nested human-readable titles now use only `title @= ...`, and duplicate `title` exports were removed from `fields.common`, `fields.specification`, and `fields.status`.
- Removed the dedicated Specification, API Reference, Project Status, and CHANGELOG regulations, Markdown realizers, and dedicated CLI render kinds.
- Removed `@narrative`, `@itemized`, `@item`, `item_document`, and other grammar/item-specific root or node decorators from the public API.
- Removed `PythonReferenceModuleRealizer`, the `shikumi-devdoc terms` command, generated Vocabulary proxy classes, and the private proxy-target compatibility layer. Canonical term classes now serve directly as IDE and `merge` references.

## V0_2_0

This was an unpublished development milestone. It expanded the documentation model and workflow with split changelog realization plus structured Specification, language-independent API Reference, and non-historical Project Status document types. These changes were carried forward into the subsequent 0.3.0 development.

version: 0.2.0

Added:

- Added repeatable Vocabulary `alias` metadata together with `deprecated` and `replacement`, allowing alternate names and deprecation relationships to be validated and rendered as semantic information.
- Added changelog `unreleased` and `breaking` semantics. An unreleased section is unique, leading, and undated; breaking entries retain their normal change category while being explicitly marked in Markdown.
- Added physical changelog partitioning with `@changelog_part(order=..., filename=...)`, allowing release history to span multiple modules while remaining one logically ordered, globally validated changelog.
- Added `filename` to changelog roots and parts. Changelog Markdown now renders to the declared files under the CLI output directory by default, while `--single-file` explicitly combines the logical changelog into the root filename.
- Added Specification regulations and Markdown realizers. Specifications model class-derived stable identities, normative levels, content, and generic named `detail` entries, with declared part filenames, optional part ordering, split output by default, and single-file realization when all parts define an order.
- Added a language-independent API Reference regulation and Markdown realizers. API entries use generic kinds, inputs, outputs, and named `detail` entries rather than language-specific exception or function semantics, and use the same part-filename/output-order model as specifications.
- Added dogfooding for the new Specification and API Reference regulations: `shikumi-devdoc` now keeps its current specification and public API reference as canonical structured sources, realizes Japanese canonical documents, and publishes separate translations under `docs/specification/` and `docs/api/`.
- Added `@condition` for explicit Specification applicability and `related @= (...)` for entity-based relationships between Specification items and API Reference entries/inputs/outputs. Related targets are actual `@spec` / `@api` Python entities rather than string identifiers, and the relationship is validated and rendered as structured documentation.
- Extended the shared `related @= (...)` writer to general-document headings. General documents validate and retain direct `@spec` / `@api` entity references as semantic information, while the standard general-document Markdown realizer deliberately leaves them out of the rendered prose.
- Added automatic root indexes to Specification and API Reference Markdown realizers. The indexes enumerate items across all parts, use part `order` when every part defines it, fall back to stable structural order otherwise, and are omitted from individual part documents.

- Added a non-historical Project Status regulation and `ProjectStatusMarkdownRealizer`. Current facts are modeled as Snapshots, future intentions as Directions, and future-facing user announcements as Notices; the realizer derives the fixed `STATUS.md` artifact name.
- Added wheel-distributed documentation resources: the complete `devdocs/` reference corpus plus this release's public README, Project Status, CHANGELOG, Specification, and API Reference. The MIT License remains distributed through project license metadata rather than being duplicated as package data.

Changed:

- Reorganized the repository dogfooding workspace from `_internal/` to `devdocs/`, separating document sources, realization inputs, and realized documents. After the canonical-boundary clarification, the workspace now uses `canonical_sources/`, `config/`, and `canonical_documents/`.
- Removed output `filename` from Specification and API Reference roots. Their standard Markdown realizers now derive `INDEX.md` from the whole document set; part filenames remain explicit, and collisions with `INDEX.md` are diagnosed during realization.
- Refactored `@condition` from a Specification-only implementation into a shared descriptor so Project Status items can also express applicability conditions as structured semantic information.
- Declared `pytest>=8.0` as the `test` optional dependency in project metadata so an sdist can reconstruct its test environment with `.[test]`.
- Changed Specification and API Reference document sources so every root/part unit is explicitly marked with `@canonical`; roots now declare only the document set, while content lives in canonical parts such as Core. Specification item identity is derived from the `@spec` class name, and API entry identity is derived from class names and nested API-entry structure. `@api(name=...)` remains available for public names that cannot be expressed as Python identifiers.
- Reorganized the public Python API so the top-level `shikumi_devdoc` namespace is a small entry point exposing the Context APIs plus `norms` and `realizers`. Norm implementation modules are private, while document-authoring APIs and standard realization APIs are collected beneath the `norms` and `realizers` namespaces respectively.
- Reorganized `norms` and `realizers` into domain namespaces such as `shikumi_devdoc.norms.specification` and `shikumi_devdoc.realizers.specification`. Short normative and kind values are grouped under dedicated namespaces such as `specification.level.MUST`, `api_reference.kind.OPERATION`, `changelog.kind.ADDED`, and `status.notice_kind.BREAKING_CHANGE`. This also allows descriptors such as `document.title` and `vocabulary.title` to keep their natural names without flat-namespace renaming.
- Removed general-document string `anchor` values and `{{#...}}` section references so canonical source no longer maintains a parallel identity separate from the Python entity. Project Status Snapshots, Directions, and Notices no longer take string ID arguments; their semantic identities are derived from Python class names. Added regression coverage proving that multiple distinct `TERM_N` placeholders can be resolved within one body.
- Changelog parts are now canonical source units in the same sense as other partitioned document sources: every `CHANGELOG_PART` requires `@canonical`, and split Markdown notices identify the canonical source of the specific part being rendered.
- Clarified `related` as a direct reference to Python class objects that are already resolvable when the descriptor expression is evaluated. The library does not resolve strings, forward references, or deferred symbolic references, and it does not impose semantic source/target direction, self-reference, or cyclicity constraints. References without a known Specification/API identity render with their fully qualified Python name.
- Redefined the documentation authority boundary: Python `@canonical` descriptions are canonical sources, while the validated realization assembled from those sources and realization context is the canonical document. Translation, localization, and distribution produce published documents outside the library's prescribed workflow. The dogfooding tree now uses `devdocs/canonical_sources/` and `devdocs/canonical_documents/`, and the intermediate-document concept has been removed.
- Changed canonical-source provenance recorded by `@canonical` to derive from Python module structure instead of a filesystem path relative to the current working directory, so realizing the same source is stable across invocation directories.

- Decoupled changelogs from Vocabulary and placeholder resolution. Changelog titles, release labels, notes, and change text are now realized as literal strings, so `{{...}}` has no special meaning in changelog source.

## V0_1_0

First public release. It establishes the core facilities for describing, validating, and realizing developer documentation from Shikumi semantic information.

version: 0.1.0

released on: 2026-09-13

Added:

- Added regulations for general documents, vocabularies, and changelogs, together with standard Markdown realizers for each.
- Added external information supplied to realizers, with reference markers in document text for project names, versions, and other values that have another canonical source.
- Added a CLI for generating term reference modules from a Vocabulary, allowing IDE navigation from `TERM_N` identifiers to human-readable term names and definitions.
- Added entity-local vocabulary references and validation that requires `TERM_N` markers in each entity to match that entity's own `vocabulary_refs` exactly.
- Added explicit canonical-source declaration with `@canonical` and support for caller-provided header comments in Markdown realizers.
- Added a dogfooding workflow that generates Japanese intermediate documents from canonical Python sources and publishes their English translations at the repository root.
- Added `TranslationSourceRealizer` and `render --translation-source` so translation-oriented intermediate Markdown can retain machine-readable metadata for `preserve_spelling` terms.
- Added stable document anchors with `anchor @= "..."` and semantic section references through `{{#anchor}}`. References are extracted automatically into `SectionReference` information, and validation rejects unknown references, duplicate anchors, and invalid anchor names.

Changed:

- Renamed the vocabulary translation-policy information from `untranslatable` to `preserve_spelling` to clarify that it means keeping a term's spelling unchanged across translations, not that the term is inherently untranslatable.
- Consolidated the generation notice and LLM publication instructions into a single repository-local `notice.toml` value. Intermediate documents include it only when `render --notice` is specified explicitly; the CLI performs no implicit notice-file discovery. Removed the repository-specific `build_docs.py` and moved term-reference and intermediate-document generation to direct CLI commands.
- Changed `render --context` from external-context file inputs to one JSON object string representing the values at realization time. This separates comparatively stable operational text in `notice.toml` from variable snapshot data, and `_internal/document_source/README.md` now records the repository-local generation procedure.
- Unified placeholder lexing, added `\{{...}}` as an explicit literal escape, preserved `${{...}}` host-language syntax, and made vocabulary-reference validation use the same lexical rules.
- Improved CLI diagnostics with severity, diagnostic code, Python source location, and semantic subject, and added Markdown structural checks for raw body headings and heading depth beyond six levels.
