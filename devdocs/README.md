# devdocs/

`devdocs/` is the authoring workspace used to dogfood this repository's own documentation system.

It separates authoritative Python canonical sources, realization-time inputs, and the canonical documents generated from them. Published documents derived through translation, localization, or distribution are repository publication concerns and live at the repository root or under `docs/`.

## Directory layout

```text
devdocs/
├── README.md
├── canonical_sources/
├── config/
│   ├── context.json
│   └── notice.toml
└── canonical_documents/
```

- `canonical_sources/` contains the authoritative Python source units that compose canonical documents.
- Specification, API Reference, STATUS, and CHANGELOG dogfood the standard field sets under `shikumi_devdoc.fields`.
- `config/` contains repository-specific realization inputs such as context and generation notices.
- `canonical_documents/` contains documents assembled by validating canonical source, injecting any required context, and realizing Markdown.
- `README.md` is the public entry point to this workspace and is itself produced from `canonical_sources/workspace/canonical.py`.

## Canonical source

The Python descriptions under `canonical_sources/` are authoritative inputs for document generation. README, Authoring Guide, Project Status, CHANGELOG, Specification, API Reference, Vocabulary, and this workspace README all keep their source units here.

README, Authoring Guide, STATUS, CHANGELOG, Specification, and API Reference use the same `@canonical_source(...)` document model. Specification and API Reference have no dedicated root/part regulations: each file is an independent canonical document. Their `INDEX.md` files are derived separately from the package-level canonical-source collection by the index realizer, using each document's `@summary(...)` metadata for the human-facing overview, so no `root.py` duplicates collection membership or exposes source paths.

Canonical sources use the foundational authoring APIs under `shikumi_devdoc.norms` and, when useful, the optional standard field sets under `shikumi_devdoc.fields`. Canonical-source metadata and shared policies come from `norms.common`; field writers and the document validation system come from `norms.document`. The standard field sets are predefined combinations of those generic primitives and may be replaced by project-local field vocabularies. Standard Markdown realization uses `shikumi_devdoc.realizers.document`. Private implementation modules are not public import paths.

The authoritative Vocabulary source is `canonical_sources/vocabulary/canonical.py`. A Vocabulary source is still an ordinary `@canonical_source(...)`; `@vocabulary` applies the semantic profile, and each direct child declares its term name with a `{{term name}}` marker at the start of the docstring after `inspect.cleandoc()`-equivalent normalization. The remaining docstring is the definition. Vocabulary terms are referenced directly through these canonical classes, so no IDE proxy module is generated.

## Realization context

`config/context.json` holds values such as project name, current release, and supported Python range that should be injected at realization time instead of being frozen into canonical source. This file is a repository workflow input, not part of the general `shikumi-devdoc` contract.

Context is not historical storage. Information that must not change later, such as past CHANGELOG versions, belongs directly in canonical source. Current README version information can come from context.

`config/notice.toml` contains the repository-specific generation notice and publication guidance embedded at the beginning of canonical documents when explicitly requested.

The CLI does not discover these files implicitly. Pass context as JSON through `--context` and the notice file through `--notice`.

## Canonical document

`canonical_documents/` is the artifact boundary consistently owned by `shikumi-devdoc`. A canonical document is the result of validating canonical source, injecting realization context where allowed, and assembling the document through a realizer.

Canonical documents are generated artifacts but are kept in Git as reviewable boundaries. Do not edit them directly. Change canonical source or realization input and regenerate instead.

## Generation

Run from the repository root:

```bash
CONTEXT="$(cat devdocs/config/context.json)"

shikumi-devdoc render glossary \
  devdocs.canonical_sources.vocabulary.canonical \
  -o devdocs/canonical_documents/GLOSSARY.md \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.readme.canonical \
  -o devdocs/canonical_documents \
  --context "$CONTEXT" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.authoring_guide \
  -o devdocs/canonical_documents/authoring_guide \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render index \
  devdocs.canonical_sources.authoring_guide \
  -o devdocs/canonical_documents/authoring_guide \
  --index-title "shikumi-devdoc Authoring Guide" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.workspace.canonical \
  -o devdocs/canonical_documents/devdocs \
  --notice devdocs/config/notice.toml

shikumi-devdoc render document \
  devdocs.canonical_sources.status.canonical \
  -o devdocs/canonical_documents \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.changelog.canonical \
  -o devdocs/canonical_documents/changelog \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.specification \
  -o devdocs/canonical_documents/specification \
  --context "$CONTEXT" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render index \
  devdocs.canonical_sources.specification \
  -o devdocs/canonical_documents/specification \
  --context "$CONTEXT" \
  --index-title "shikumi-devdoc Specification" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.api_reference \
  -o devdocs/canonical_documents/api \
  --context "$CONTEXT" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render index \
  devdocs.canonical_sources.api_reference \
  -o devdocs/canonical_documents/api \
  --context "$CONTEXT" \
  --index-title "shikumi-devdoc API Reference" \
  --notice devdocs/config/notice.toml \
  --translation-source
```

`merge_policy` declares which merge sources a canonical document accepts: `"all"`, `"local"`, `"external"`, or `"forbidden"`. This repository uses `"forbidden"` for CHANGELOG so historical snapshots cannot change through later local or external values, `"local"` for self-contained documents that may reuse canonical-local information, and `"all"` where realization context is intentionally part of the document. The legacy `placeholders` boolean is deprecated as of 0.3.2 and scheduled for removal in 1.0.0. Class merge targets use the shortest unambiguous suffix of their Python identity, with longer qualification available when names collide; field bindings use their `@=` left-hand names and may be given explicit aliases when needed.

## Tests

To reconstruct the test environment from an sdist:

```bash
python -m pip install '.[test]'
pytest
```

The `test` extra declares `pytest>=8.0`; pytest is not a runtime dependency.

Release distribution verification is performed locally rather than relying on hosted CI. With the `build` frontend available, run:

```bash
python scripts/check_dist.py
```

This builds the wheel and sdist and checks archive contents, installed-package behavior, the CLI, `pip check`, and dogfood rendering through the installed wheel. If the required Shikumi release is being prepared at the same time and is not yet available on PyPI, provide its source tree explicitly:

```bash
python scripts/check_dist.py --shikumi-source /path/to/shikumi
```

## Published documents

Published documents are derivatives of canonical documents. `shikumi-devdoc` does not prescribe the publication workflow.

This repository translates the Japanese canonical documents into English and places them at the repository root, under `docs/authoring_guide/`, under `docs/specification/`, under `docs/api/`, and in this `devdocs/README.md`. Generation notices and `shikumi-devdoc:translation-metadata` are removed from published output.

## Distribution in the wheel

The complete `devdocs/` tree is included in the wheel as a reference corpus under `shikumi_devdoc/resources/devdocs/`. Published README, STATUS, CHANGELOG, and `docs/` are included separately under `shikumi_devdoc/resources/published_docs/`.

These resources are not importable public API. The MIT License is distributed through normal wheel license metadata.

## Distribution in the sdist

The sdist is a complete source distribution for reconstructing and verifying this release. In addition to the implementation, it includes `tests/`, `devdocs/`, published `docs/`, `scripts/`, root published documents, the license, and build metadata. `scripts/check_dist.py` itself is included so the same distribution verification can be re-run from the downloaded source distribution.

File selection does not enumerate every included path. Instead, it relies on Hatchling's default behavior of respecting VCS ignore rules and includes the release source by default. Repository-operation-only content such as `.github/` is explicitly excluded. Caches, virtual environments, `dist/`, IDE metadata, and other local or generated artifacts remain excluded by `.gitignore`.
