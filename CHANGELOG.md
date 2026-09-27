# shikumi-devdoc Changelog

Changes included in public releases of `shikumi-devdoc` are recorded here.

## Unreleased

Changes planned for the next public release.

### Added

- Added repeatable Vocabulary `alias` metadata together with `deprecated` and `replacement`, allowing alternate names and deprecation relationships to be validated and rendered as semantic information.
- Added changelog `unreleased` and `breaking` semantics. An unreleased section is unique, leading, and undated; breaking entries retain their normal change category while being explicitly marked in Markdown.
- Added physical changelog partitioning with `@changelog_part(order=...)`, allowing release history to span multiple modules while remaining one logically ordered, globally validated changelog.

## 0.1.0 - 2026-09-13

First public release. It establishes the core facilities for describing, validating, and realizing developer documentation from Shikumi semantic information.

### Added

- Added regulations for general documents, vocabularies, and changelogs, together with standard Markdown realizers for each.
- Added external information supplied to realizers, with reference markers in document text for project names, versions, and other values that have another canonical source.
- Added a CLI for generating term reference modules from a Vocabulary, allowing IDE navigation from `TERM_N` identifiers to human-readable term names and definitions.
- Added entity-local vocabulary references and validation that requires `TERM_N` markers in each entity to match that entity's own `vocabulary_refs` exactly.
- Added explicit canonical-source declaration with `@canonical` and support for caller-provided header comments in Markdown realizers.
- Added a dogfooding workflow that generates Japanese intermediate documents from canonical Python sources and publishes their English translations at the repository root.
- Added `TranslationSourceRealizer` and `render --translation-source` so translation-oriented intermediate Markdown can retain machine-readable metadata for `preserve_spelling` terms.
- Added stable document anchors with `anchor @= "..."` and semantic section references through `{{#anchor}}`. References are extracted automatically into `SectionReference` information, and validation rejects unknown references, duplicate anchors, and invalid anchor names.

### Changed

- Renamed the vocabulary translation-policy information from `untranslatable` to `preserve_spelling` to clarify that it means keeping a term's spelling unchanged across translations, not that the term is inherently untranslatable.
- Consolidated the generation notice and LLM publication instructions into a single repository-local `notice.toml` value. Intermediate documents include it only when `render --notice` is specified explicitly; the CLI performs no implicit notice-file discovery. Removed the repository-specific `build_docs.py` and moved term-reference and intermediate-document generation to direct CLI commands.
- Changed `render --context` from external-context file inputs to one JSON object string representing the values at realization time. This separates comparatively stable operational text in `notice.toml` from variable snapshot data, and `_internal/document_source/README.md` now records the repository-local generation procedure.
- Unified placeholder lexing, added `\{{...}}` as an explicit literal escape, preserved `${{...}}` host-language syntax, and made vocabulary-reference validation use the same lexical rules.
- Improved CLI diagnostics with severity, diagnostic code, Python source location, and semantic subject, and added Markdown structural checks for raw body headings and heading depth beyond six levels.
