# shikumi-devdoc

`shikumi-devdoc` is a library for describing developer documentation as Python canonical source with semantic structure, validating it with [Shikumi](https://pypi.org/project/shikumi/), and realizing it as Markdown canonical documents.

It provides two foundations: Vocabulary and a common canonical document model. Terminology and spelling live in Vocabulary, while README, Authoring Guide, Project Status, CHANGELOG, Specification, API Reference, and similar documents use the same document model built from nested classes, docstring templates, and author-defined fields.

## What it is for

Use `shikumi-devdoc` when continuously maintained developer documentation should keep its authoritative source as validated semantic information in Python and produce reproducible canonical documents with the required realization context.

| Purpose | Foundation |
| --- | --- |
| Manage terminology names and concept definitions in one place | Vocabulary |
| Compose README, Authoring Guide, Project Status, CHANGELOG, Specification, API Reference, and similar documents | canonical document model |

Specification and API Reference are not built-in document kinds. Domain-specific meaning belongs to the author's field vocabulary. You can reuse the standard field sets under `shikumi_devdoc.fields` or define project-local fields.

## Minimal usage

Install from PyPI:

```bash
pip install shikumi-devdoc
```

A minimal canonical source needs only a root class decorated with `@canonical_source(...)` and a nested class beneath it.

```python
from shikumi_devdoc.norms.common import canonical_source

@canonical_source("Example", filename="example.md", merge_policy="local", heading="identity")
class EXAMPLE:
    class Introduction:
        '''Hello from shikumi-devdoc.'''
```

Pass the module to the CLI to generate a canonical document:

```bash
shikumi-devdoc render document myproject.example -o build/
```

The generated Markdown is:

```markdown
# Example

## Introduction

Hello from shikumi-devdoc.
```

Nested classes become child document nodes without additional decorators, and their nesting maps to heading depth. Context, fields, Vocabulary, indexes, and other features can be added to the same model when needed.

## Core model

`shikumi-devdoc` does not treat hand-edited Markdown as the authoritative source. A canonical document is established through validation and realization from canonical source plus realization context.

```text
canonical source
      + realization context
        ↓ Shikumi interpretation and validation
     SemanticView
        ↓ shikumi-devdoc realizer
canonical document
        ↓ project-specific publication workflow
  published document
```

`shikumi-devdoc` consistently owns the workflow through the canonical-document boundary. Translation, localization, prose editing, media conversion, and distribution belong to a project-specific publication workflow that produces published documents.

A canonical document uses one common document node / template / field / merge model. Nested classes define document hierarchy, docstrings provide body templates, and fields carry structured supplemental information. Prose such as background explanations can remain in docstrings, while information that matters structurally can be separated into fields.

The generic document core does not embed Specification or API Reference semantics. New document uses are expressed by combining the required field vocabulary and presentations with the same foundation rather than introducing a separate grammar.

## Vocabulary and structured information

Vocabulary keeps terminology names and concept definitions as canonical source. Each Vocabulary term has a stable `TERM_N` class identity, so consuming documents can reference the term class instead of duplicating the human-facing term string.

```python
merge @= TERMS.TERM_001
```

Templates can normally use a short reference such as `{{TERM_001}}`. If multiple Vocabularies contribute the same identity, qualify the Python identity only as far as needed to disambiguate it. See the Specification for the precise name-resolution rules.

Document-specific structured information is declared as fields. Authors can define project-local field vocabularies or reuse common standard field sets from `shikumi_devdoc.fields`. The generic core does not own the domain meaning of those fields.

Docstrings, `prose_field`, and `title @= ...` are template-bearing content and can use local references and external placeholders. A field written with `name @= value` is automatically available to templates on the same node as `{{name}}`; `merge` adds class targets, literal strings, or explicit aliases to the same local namespace. `merge_policy` controls which sources may participate: `"all"` allows local and external merge, `"local"` allows only local references, `"external"` allows only realization context, and `"forbidden"` allows neither. Use `"forbidden"` for snapshot-style sources such as a CHANGELOG when later changes must not rewrite historical content. The old `placeholders` boolean is deprecated in 0.3.2 and will be removed in 1.0.0; `True` maps to `"all"` and `False` maps to `"local"`.

Ordinary `field`, `list_field`, `table_field`, and `test_target_field` values themselves remain literal content. `test_target_field` separates literal text that ordinary tests should inspect directly; Markdown fences and language markers belong in the surrounding template. Use `reference_field` when a Python object relationship should realize as a logical Markdown reference; the standard `related` field is a convenience field built on that presentation. Unreferenced fields can be appended to the body with `APPEND` or retained as source-only semantic information with `IGNORE`.

## Documentation workflows with LLMs

One intended workflow is that people own intent, decisions, and review while an LLM assists with ongoing canonical-source maintenance.

The design therefore favors explicit meaning, mechanical validation, and stable regeneration of canonical documents rather than minimizing authoring syntax alone. At the same time, using an LLM is not a reason to accept unnecessary complexity, duplicated semantics, or abstractions without a concrete need.

## Documentation

`shikumi-devdoc` dogfoods its own documentation system.

- [Authoring Guide](docs/authoring_guide/INDEX.md): practical guidance for designing and maintaining canonical source.
- [Specification](docs/specification/INDEX.md): guaranteed behavior and constraints.
- [API Reference](docs/api/INDEX.md): public interfaces.
- [Project Status](STATUS.md): current state and forward-looking notices.
- [CHANGELOG](CHANGELOG.md): past changes.
- [devdocs workspace](devdocs/README.md): this repository's documentation-generation workspace.
- [`devdocs/canonical_sources/`](devdocs/canonical_sources/): the canonical sources used by this project.
- [`devdocs/canonical_documents/`](devdocs/canonical_documents/): Japanese canonical documents generated from validated source and realization context.

The `devdocs/` tree also serves as a reference corpus for the authoring API. Comparing a canonical source with its corresponding canonical document shows the relationship between authoring, context injection, and realization output.

English published documents at the repository root and under `docs/` are produced by a separate publication workflow using the Japanese canonical documents as input. That translation and publication process is not a feature of `shikumi-devdoc` itself.

## Version

Current version: `0.3.2`. Supported Python: `>=3.11`. See [`STATUS.md`](STATUS.md) for the current development stage and notices.

## License

`shikumi-devdoc` is available under the MIT License. See [`LICENSE`](LICENSE).
