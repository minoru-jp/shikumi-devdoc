# shikumi-devdoc

`shikumi-devdoc` is a library for **growing specifications and design documents together with the implementation**.

Developer documentation such as README, Specification, API Reference, and CHANGELOG is written not as standalone Markdown files, but as Python **canonical source** with meaning and structure.

It is intended for projects that want documentation to remain an authoritative source that is referenced and updated throughout development, rather than something organized only after implementation is complete.

## Where it fits

`shikumi-devdoc` does not provide a particular development process by itself.

Instead, it provides a documentation foundation for development styles that place specifications and design at the center of the work.

For example, it can be combined with approaches such as:

- **Spec-Driven Development (SDD)**  
  Treat specifications not as temporary material written before implementation, but as an authoritative development source that evolves together with the implementation.

- **Docs as Code**  
  Manage documentation in the same repository as code, and treat changes, reviews, and history as part of software development.

- **LLM-assisted development**  
  Maintain the specifications, design, and constraints given to an LLM as development assets with meaning and structure instead of scattered prose.

In SDD in particular, the challenge is not merely writing a specification, but **keeping the specification aligned with the implementation over time**.

`shikumi-devdoc` provides a way to keep that authoritative source in Python so that it remains workable for both people and LLMs.

## This project is its own sample

`shikumi-devdoc` uses `shikumi-devdoc` to manage its own README, Specification, API Reference, CHANGELOG, and other documents.

The canonical sources actually used by this project are under [`devdocs/canonical_sources/`](https://github.com/minoru-jp/shikumi-devdoc/tree/main/devdocs/canonical_sources).

The following two examples show documents with very different characteristics.

### README: prose-first documentation

Most of a README is ordinary prose.

Its canonical source can preserve that character directly.

````python
from shikumi_devdoc.norms.common import IGNORE, canonical_source
from shikumi_devdoc.norms.document import test_target_field, title


example_source = test_target_field("example source")


@canonical_source(
    "{{project.name}}",
    filename="README.md",
    merge_policy="all",
    unreferenced_fields=IGNORE,
    heading="title",
)
class SECTION_001:
    r"""
    `{{project.name}}` は、仕様や設計文書を
    実装と一緒に育てるためのライブラリです。

    ```python
    {{example_source}}
    ```
    """

    example_source @= r"""
    from shikumi_devdoc.norms.common import canonical_source


    @canonical_source("Example", filename="example.md", merge_policy="local", heading="identity")
    class EXAMPLE:
        class Introduction:
            "Hello from shikumi-devdoc."
    """

    class SECTION_002:
        """このプロジェクト自身の文書も、この仕組みで管理しています。"""

        title @= "このプロジェクト自身がサンプルです"
````

The document hierarchy is represented by Python class structure, while the body can be written directly as docstrings.

There is no need to decompose prose-oriented documentation into unnecessarily fine-grained data structures.

You can keep a README free-form while giving meaning and structure only to the parts that need them.

### Specification: documentation as a collection of items

A Specification has a different shape: the individual specification items matter as much as the prose itself.

This project's own Specification uses the same canonical-source mechanism.

```python
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.fields.specification import MUST, level
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source(
    "Structured fields",
    filename="specification.md",
    order=50,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    class SPEC_001:
        """canonical root 内の class は {{TERM_006}} として解釈されなければならない。"""

        merge @= TERMS.TERM_006
        title @= "Class-derived document-node identity"
        level @= MUST
```

README and Specification look and behave quite differently.

One is centered on free-form prose; the other is a collection of semantically meaningful items.

`shikumi-devdoc` does not force both into one specialized document format. They use the same foundation while choosing a shape appropriate to each document.

```text
README
  └─ free-form prose first
       └─ structure only where needed

Specification
  └─ collection of items first
       └─ meaning attached to each item
```

Specification and API Reference are not special document grammars.

They are built on the same canonical-source model by combining the meanings required by each document.

## Referencing and inserting values

Templates in canonical source can reference separately held values as `{{name}}` instead of containing only fixed prose.

Those values can come from a field defined on the same node, a local reference brought in from another canonical source, or external context supplied at realization time.

### Refer to a value defined on the same node

A field defined on a node with `name @= value` can be referenced as `{{name}}` from that node's docstring or other template-bearing content.

The `example_source` in the README example above uses exactly this mechanism. The code example is kept as independent literal text rather than duplicated directly in the prose, and the template references it where it should appear.

`test_target_field` can be used to **separate code, configuration, commands, expected output, or other text that ordinary tests should reference directly**. The sample code in this README is itself separated from the canonical source as a `test_target_field`; ordinary pytest tests compare it with the corresponding example module and then validate and render that module.

Separating a value with `test_target_field` does not automatically create or run a test, and it does not imply test coverage. What should be verified and how it should be verified remains part of the project's ordinary test design. `test_target_field` only makes the text an independent unit in the authoritative source that tests can address directly.

### From another canonical source

An object from another canonical source can also be brought into the same node as a local reference.

Vocabulary, for example, uses this mechanism so that shared terminology can be defined once and reused across documents.

```python
merge @= TERMS.TERM_001
```

Instead of copying terms and definitions directly into prose, documents can retain relationships between authoritative sources.

Vocabulary is one convenient use of this mechanism, but the mechanism itself is not specific to Vocabulary.

### From external context

Values can also be supplied from outside the canonical source.

Typical examples include the current version shown in a README or other values determined at generation time.

```text
canonical source
       +
external context
       ↓
     document
```

These values do not have to be frozen into the canonical source itself; they can be supplied as the context in which the document is generated.

## Choose insertion channels with merge policy

Fields defined directly on the same node remain available to templates regardless of `merge_policy`.

`merge_policy` constrains two explicit ways of bringing values into template-bearing content:

- local merge through `merge @= ...`
- external context supplied at realization time

| policy | `merge @= ...` | external context |
| --- | --- | --- |
| `all` | allowed | allowed |
| `local` | allowed | not used |
| `external` | not used | allowed |
| `forbidden` | not used | not used |

This README uses `all` because it uses both external context and local merge. The Specification uses `local` because it uses local merge without external context. CHANGELOG uses `forbidden` because it uses neither. These are choices about the insertion channels used by each canonical source; they do not determine the document type itself.

`merge_policy` also does not track the provenance of ordinary Python values. Once a value is bound directly on the node with `name @= value`, it is treated as that node's own field regardless of where the value originated before Python evaluated the assignment.

See the [Authoring Guide](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/authoring_guide/advanced-authoring.md) and [Specification](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/specification/core.md) for the exact rules of all four policies.

## Extensible by design

The meanings and Markdown output provided by `shikumi-devdoc` are not the only possible uses of the model.

The library is built on [Shikumi](https://github.com/minoru-jp/shikumi). See the [Shikumi documentation](https://github.com/minoru-jp/shikumi/tree/main/docs) for the underlying mechanisms for semantic annotation, structuring, validation, and realization.

On that foundation, `shikumi-devdoc` can be extended in two directions.

### Express project-specific meaning

You are not limited to the meanings provided by `shikumi-devdoc`.

Project-specific descriptors can add meaning to the same canonical source.

For example, a development process can represent information such as Requirement, Risk, Decision, Owner, Component, or Review status.

Instead of adapting the project to a fixed document format, you can **give documents the meaning that the project itself needs**.

### Produce formats other than Markdown

`shikumi-devdoc` provides a Markdown realizer.

When another format is needed, a custom realizer can be implemented using Shikumi's realization model.

Because the meaning held by canonical source is separate from the final output format, the same authoritative source can be used to produce other artifacts as well.

## Minimal usage

Install from PyPI:

```bash
pip install shikumi-devdoc
```

A minimal canonical source needs only a root class and a nested class.

```python
from shikumi_devdoc.norms.common import canonical_source


@canonical_source(
    "Example", filename="example.md", merge_policy="local", heading="identity"
)
class EXAMPLE:
    class Introduction:
        """Hello from shikumi-devdoc."""
```

Pass the module to the CLI:

```bash
shikumi-devdoc render document myproject.example -o build/
```

The generated Markdown is:

```markdown
# Example

## Introduction

Hello from shikumi-devdoc.
```

From there, structured information, insertion, cross-document references, and other features can be added as needed.

> [!IMPORTANT]
> Canonical source is imported as a Python module. Do not execute an untrusted Python module as documentation input.

### `@=` notation and mypy

Shikumi itself does not require `@=`. `shikumi-devdoc` intentionally uses the `shikumi.standard`-style `name @= value` notation because it keeps canonical source readable as document source.

Checking this style with mypy requires an additional canonical-source-package setting. See [`STATUS_008`](https://github.com/minoru-jp/shikumi-devdoc/blob/main/STATUS.md#status_008) for the rationale, the configuration recipe, and the scope of the suppression.

## Documentation

This repository's documentation is itself a working example of `shikumi-devdoc`.

- [Authoring Guide](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/authoring_guide/INDEX.md): practical guidance for designing and maintaining canonical source.
- [Specification](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/specification/INDEX.md): behavior and constraints guaranteed by `shikumi-devdoc`.
- [API Reference](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/api/INDEX.md): public interfaces.
- [Project Status](https://github.com/minoru-jp/shikumi-devdoc/blob/main/STATUS.md): current development status.
- [CHANGELOG](https://github.com/minoru-jp/shikumi-devdoc/blob/main/CHANGELOG.md): change history.
- [`devdocs/canonical_sources/`](https://github.com/minoru-jp/shikumi-devdoc/tree/main/devdocs/canonical_sources): canonical sources used by this project itself.
- [`devdocs/canonical_documents/`](https://github.com/minoru-jp/shikumi-devdoc/tree/main/devdocs/canonical_documents): Japanese canonical documents generated from canonical source.
- [devdocs workspace](https://github.com/minoru-jp/shikumi-devdoc/blob/main/devdocs/README.md): how this repository generates and manages canonical documents.

Comparing canonical source with the generated documents shows how `shikumi-devdoc` is used in practice.

English documents at the repository root and under `docs/` are produced by a separate publication workflow using the Japanese canonical documents as input. That translation and publication process is not itself a feature of `shikumi-devdoc`.

## Version

Current version: `0.3.5`

Supported Python: `>=3.11`

See [`STATUS.md`](https://github.com/minoru-jp/shikumi-devdoc/blob/main/STATUS.md) for the current development stage and compatibility information.

## License

`shikumi-devdoc` is available under the MIT License.

See [`LICENSE`](https://github.com/minoru-jp/shikumi-devdoc/blob/main/LICENSE).
