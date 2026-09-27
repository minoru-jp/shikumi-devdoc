# shikumi-devdoc

`shikumi-devdoc` is a Python library that uses [Shikumi](https://pypi.org/project/shikumi/) to provide regulations and realizers for describing, validating, and realizing public project documentation from semantic information.

Documents, vocabulary, and changelogs can be described with Python as their canonical source and realized as Markdown. Values that already have another canonical source, such as a project name or version, are supplied externally instead of being duplicated in document source code.

The current version is `0.1.0`. Python `>=3.11` is required.

## Purpose

`shikumi-devdoc` works with the semantic structure behind completed Markdown rather than treating the Markdown itself as the primary source.

The basic flow is:

```text
Python description body
    ↓ interpretation and validation by Shikumi
SemanticView
    ↓ shikumi-devdoc realizer
Japanese Markdown
    ↓ translation when needed
Public documentation
```

Keeping the canonical source in Python makes hierarchy, vocabulary references, change categories, and similar constraints mechanically verifiable. At the same time, generated Japanese Markdown can be committed as an intermediate document that people can inspect directly.

## Regulations and realizers

The initial release provides three documentation systems:

- **Documents**: general developer documentation with heading hierarchy and body text.
- **Vocabulary**: vocabulary sources with term names and definitions, with selective realization into a public glossary.
- **Changelogs**: structured release histories containing releases and change entries.

Standard Markdown realizers are provided for all three. Vocabulary can also be realized as a Python term-reference module so that developers can inspect the meaning of `TERM_N` identifiers through IDE navigation.

## Installation

Install from PyPI with:

```bash
pip install shikumi-devdoc
```

`shikumi-devdoc` depends on `shikumi`. Shikumi provides the semantic interpretation and validation foundation; this library builds developer-documentation regulations and realizers on top of it.

## Documents

A general document is described as a hierarchy of `TITLE_N` classes. The outermost entity is decorated with `@canonical` to state explicitly that the description body is the canonical source of the artifact.

```python
from shikumi_devdoc.norms.document import canonical, title


@canonical
@title("Example")
class TITLE_1:
    r'''Project overview.'''

    @title("Install")
    class TITLE_2:
        r'''Installation instructions.'''
```

The value passed to `@title(...)` becomes the heading, and the class docstring becomes the body. Nested `TITLE_N` classes are realized as nested Markdown headings. When a section link must survive heading renames, use [stable section references](#document-anchors).

### Validation and realization

Validate a description body with the `document` regulation, then realize it with `DocumentMarkdownRealizer` or `document_markdown.MarkdownRealizer`.

```python
from shikumi_devdoc.norms.document import document
from shikumi_devdoc.realizers import DocumentMarkdownRealizer

result = document.validate(document_source, placement=())
if not result.is_valid:
    raise RuntimeError(result.diagnostics)

realizer = DocumentMarkdownRealizer()
check = realizer.check(result.view)
if not check.is_realizable:
    raise RuntimeError(check.diagnostics)

markdown = realizer.realize(result.view)
```

Validation checks heading structure, canonical-source declaration, information cardinality, vocabulary-reference consistency, and related semantic constraints. The realizer's `check()` method verifies realization concerns such as unresolved reference markers. Raw ATX headings written directly in a body are reported as warnings because they bypass the semantic hierarchy, while heading depth beyond six levels is an error because Markdown cannot represent it as an ATX heading. The CLI renders diagnostics with severity, diagnostic code, source location, and semantic subject when available.

<a id="document-anchors"></a>

### Stable section references

To refer to a heading semantically, attach `anchor @= "..."` to the target. The anchor is independent of the displayed heading text, so renaming the heading does not change the reference identity.

```python
from shikumi_devdoc.norms.document import anchor, canonical, title


@canonical
@title("Guide")
class TITLE_1:
    r'''See {{#installation}}.'''

    @title("Installation")
    class TITLE_2:
        r'''Installation instructions.'''
        anchor @= "installation"
```

`{{#installation}}` in a body is realized as a Markdown link to the `Installation` heading. The referring entity does not need a separate declaration such as `section_refs`; `@title` extracts references from the body automatically and stores them in the semantic view as `SectionReference` information. Validation rejects unknown references, duplicate anchors, and invalid anchor names.

The Markdown realizer emits an explicit HTML `id` for each anchor instead of relying on platform-specific heading slugs. Section-reference markers are body-only and are not allowed in heading titles.

## External information

Project names, versions, repository data, and other values that already have another canonical source are supplied to the realizer as external information rather than duplicated in document source code.

Documents refer to those values with reference markers. For example, `{{PROJECT.name}}` and `{{PROJECT.version}}` use dotted paths to address values.

```python
from shikumi_devdoc.realizers import DocumentMarkdownRealizer

realizer = DocumentMarkdownRealizer(
    {
        "PROJECT": {
            "name": "example",
            "version": "0.1.0",
        }
    }
)
```

To construct the same context directly from a JSON string, use `from_json()`:

```python
realizer = DocumentMarkdownRealizer.from_json(
    '{"PROJECT":{"name":"example","version":"0.1.0"}}'
)
```

Unknown references are reported by `check()` instead of being silently replaced with empty text. Values may be strings or other JSON-compatible arrays and objects.

Use `\{{...}}` in the Python source when literal double braces are required. The backslash is removed during realization without resolving the marker. `${{...}}` is also treated as literal host-language syntax, so GitHub Actions expressions can appear in developer documentation without colliding with devdoc placeholders.

## Vocabulary

A vocabulary uses `VOCABULARY` as its outermost class and places `TERM_N` classes directly beneath it. The value passed to `@term(...)` is the human-readable term name, while the docstring is its definition.

```python
from shikumi_devdoc.norms.vocabulary import (
    alias,
    canonical,
    deprecated,
    glossary,
    preserve_spelling,
    replacement,
    term,
    title,
)


@canonical
@title("Example Glossary")
class VOCABULARY:
    r'''Terms used by Example.'''

    @term("Widget")
    class TERM_1:
        r'''A reusable component.'''
        glossary @= True
        alias @= "Component"
        alias @= "UI Widget"
```

Only terms with `glossary @= True` are emitted by the standard glossary Markdown realizer. Internal vocabulary can therefore remain in the canonical vocabulary source without appearing in the public glossary.

Use **preserve spelling** when a term name must keep exactly the same spelling after translation.

```python
@term("Shikumi")
class TERM_2:
    r'''The name of the Shikumi concept.'''
    preserve_spelling @= True
```

`preserve_spelling @= True` does not mean that the term is impossible to translate. It records that the term name itself must remain unchanged when the surrounding document is translated. The standard glossary Markdown realizer does not act on this value directly. For translation sources, wrap the Markdown realizer with `TranslationSourceRealizer`, or use `shikumi-devdoc render --translation-source`; preserve-spelling terms are then embedded as machine-readable translation metadata in the intermediate Markdown.

A term may declare multiple alternate names with `alias @= "..."`. Aliases must not collide with canonical term names or other aliases in the same Vocabulary. A term retained for compatibility can be marked with `deprecated @= True`; when a preferred successor exists, `replacement @= "NewTerm"` names another canonical term in the same Vocabulary.

```python
@term("Widget")
class TERM_1:
    r'''The current term.'''
    glossary @= True

@term("OldWidget")
class TERM_2:
    r'''The former term.'''
    glossary @= True
    deprecated @= True
    replacement @= "Widget"
```

`replacement` requires `deprecated @= True`. Unknown targets, self-replacement, and alias-only targets are rejected. The standard glossary realizer displays aliases and marks deprecated public terms together with their replacement when one is present.

### Term reference modules

A canonical vocabulary can keep stable, semantically neutral identifiers such as `TERM_1` and `TERM_2`. That is useful for the canonical source, but those identifiers alone are difficult for a person to interpret when referenced from another document source.

`shikumi-devdoc` can therefore generate a Python term-reference module from the vocabulary's `SemanticView`. Each generated `TERM_N` class contains the term name and definition in its docstring, allowing IDE definition navigation and hover information to reveal the meaning immediately.

```bash
shikumi-devdoc terms my_project.docs.vocabulary.canonical \
  -o my_project/docs/vocabulary/terms.py
```

The output module name and location are chosen by the consuming project. If the generated file is named `terms.py`, a document can use it like this:

```python
from my_project.docs.vocabulary import terms
from shikumi_devdoc.norms.document import (
    canonical,
    title,
    vocabulary,
    vocabulary_refs,
)


@canonical
@vocabulary(terms)
@title("API Reference")
class TITLE_1:
    r'''The public API exposes {{TERM_1}}.'''

    vocabulary_refs @= (terms.TERM_1,)
```

`@vocabulary(terms)` follows the generated module back to the canonical Vocabulary and uses it to resolve `TERM_N` markers during realization. Proxy classes passed through `vocabulary_refs` are likewise resolved back to their canonical `VOCABULARY.TERM_N` classes, preserving semantic identity.

### Local vocabulary references

`vocabulary_refs` should not be collected at the document root. Place each reference on the entity that actually uses the term.

```python
@title("Section")
class TITLE_2:
    r'''This section uses {{TERM_1}}.'''

    vocabulary_refs @= (terms.TERM_1,)
```

For every entity, the validator requires the set of `TERM_N` markers appearing in that entity's title and body to match exactly the set in that entity's own `vocabulary_refs`. References are not inherited between parent and child entities. Repeating the same `TERM_N` in the text still requires only one entry in `vocabulary_refs`.

This redundancy is intentional. `TERM_N` reference markers are used by the machine during realization, while `vocabulary_refs` gives a human a direct IDE path to the canonical term definition. The validator guarantees that the two stay synchronized.

## Changelogs

A changelog is described in three levels: `CHANGELOG`, `RELEASE_N`, and `CHANGE_N`. Change categories are `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`.

```python
from shikumi_devdoc.norms.changelog import (
    ADDED,
    CHANGED,
    breaking,
    canonical,
    change,
    changelog,
    release,
    released_on,
    unreleased,
)


@canonical
@changelog("Example Changelog")
class CHANGELOG:
    r'''Release history for Example.'''

    @release()
    class RELEASE_1:
        r'''Changes planned for the next release.'''
        unreleased @= True

        @change(CHANGED)
        class CHANGE_1:
            r'''Changed the wire format.'''
            breaking @= True

    @release("0.1.0")
    class RELEASE_2:
        r'''First public release.'''
        released_on @= "2026-09-13"

        @change(ADDED)
        class CHANGE_1:
            r'''Added the initial document system.'''
```

The Markdown realizer groups change entries by category within each release. As with documents, a changelog may use `@vocabulary(terms)` and `vocabulary_refs`; vocabulary references are validated locally on the release or change entity where they are used.

Pending changes can be represented by one leading `@release()` entry with `unreleased @= True`. It must be the first release entry and must not have `released_on`. Individual `CHANGE_N` entries can use `breaking @= True`; the Markdown realizer keeps the normal change category and marks that bullet as breaking.

A changelog can grow indefinitely in a healthy long-lived project, so its canonical source may be physically split across modules without splitting the logical changelog. Releases directly under `CHANGELOG` remain first. Releases stored elsewhere go under a top-level `CHANGELOG_PART` decorated with `@changelog_part(order=...)`.

```python
# released.py
from shikumi_devdoc.norms.changelog import (
    ADDED,
    change,
    changelog_part,
    release,
    released_on,
)


@changelog_part(order=10)
class CHANGELOG_PART:
    @release("1.0.0")
    class RELEASE_1:
        r'''First stable release.'''
        released_on @= "2026-01-01"

        @change(ADDED)
        class CHANGE_1:
            r'''Added the initial feature set.'''
```

Validate or render the changelog package rather than an individual module. The logical order is: releases directly under `CHANGELOG`, then `CHANGELOG_PART` containers by ascending `order`, then source order within each part. Filenames do not affect release order. Duplicate part orders, duplicate release labels, and multiple `Unreleased` sections are checked across the whole package. The original single-module form remains valid.

## Canonical sources and generated artifacts

The outermost entity of a document, vocabulary, or changelog is decorated with `@canonical`. This declaration remains explicit even when the location could be inferred, because making the canonical-source contract visible in source code is useful to a human reader.

Markdown realizers can place an arbitrary operational comment at the beginning of a generated artifact. The wording of that comment is not defined by `shikumi-devdoc` itself. A consuming project defines the content operationally and supplies it when rendering an intermediate document.

This repository keeps the generation notice and the LLM publication instructions together in `_internal/document_source/notice.toml` as a single `[notice].content` value. Passing that file explicitly with `shikumi-devdoc render --notice ...` causes the CLI to replace `{canonical_source}` with the canonical source path and pass the complete content to the Markdown realizer as its leading comment. The CLI does not search for a notice file automatically.

This keeps project-specific operational language out of the library implementation while allowing each project to carry the instructions required by its own generation and publication workflow directly in its intermediate documents.

## Recommended documentation workflow

When Japanese is the source language and English is the public language, the recommended workflow has three layers:

```text
_internal/document_source/.../canonical.py
    ↓ realization
_internal/document_build/ja/...md
    ↓ translation
README.md and other public English documents
```

`canonical.py` is the semantic canonical source, the Japanese Markdown is a human-readable intermediate artifact, and the top-level English Markdown is the published artifact.

The intermediate document may be committed to Git. It is not merely a temporary build file: it provides an inspection boundary for checking that the regulation was realized as intended and that the Japanese source text is correct before translation. It must not be edited directly.

Translation into public English documentation is treated as a publication step mediated by an LLM rather than as a mechanical build step. This repository stores generation and publication instructions in `notice.content` in `_internal/document_source/notice.toml`, supplied explicitly with `--notice`.

For translation-bound intermediates, `--translation-source` can additionally embed a `shikumi-devdoc:translation-metadata` HTML comment. That comment carries semantic policy such as the exact terms marked with `preserve_spelling @= True`, so the intermediate Markdown does not lose that information at realization time. Translation metadata and operational comments are not publication content and should be omitted from the public document.

## Repository dogfooding

`shikumi-devdoc` uses this same workflow to build its own README and CHANGELOG.

```text
_internal/
├── document_source/
│   ├── README.md
│   ├── notice.toml
│   ├── readme/
│   │   └── canonical.py
│   ├── changelog/
│   │   ├── canonical.py
│   │   └── released.py
│   └── vocabulary/
│       ├── canonical.py
│       └── terms.py
└── document_build/
    └── ja/
        ├── README.md
        └── CHANGELOG.md
```

`_internal/document_source/README.md` briefly explains the files in this directory and the local intermediate-document workflow. `notice.toml` contains operational text that changes rarely.

Project name, version, and other values that represent the current rendering snapshot are not stored as another context file. Instead, the caller assembles the required values into one JSON object and passes that JSON string with `--context`. For example:

```bash
CONTEXT='{"project":{"name":"shikumi-devdoc","version":"0.1.0","requires-python":">=3.11"}}'

shikumi-devdoc terms \
  _internal.document_source.vocabulary.canonical \
  -o _internal/document_source/vocabulary/terms.py

shikumi-devdoc render document \
  _internal.document_source.readme.canonical \
  -o _internal/document_build/ja/README.md \
  --context "$CONTEXT" \
  --notice _internal/document_source/notice.toml \
  --translation-source

shikumi-devdoc render changelog \
  _internal.document_source.changelog \
  -o _internal/document_build/ja/CHANGELOG.md \
  --context "$CONTEXT" \
  --notice _internal/document_source/notice.toml \
  --translation-source
```

`--notice` explicitly names a file containing comparatively stable operational text, and no notice file is discovered implicitly. `--context` accepts one JSON object string representing the external-information snapshot for that realization. `--translation-source` preserves translation-relevant semantic policy in the intermediate artifact. How the caller obtains context values is deliberately outside `shikumi-devdoc`. The top-level `README.md` and `CHANGELOG.md` are then produced by translating the Japanese intermediates with an LLM according to the embedded instructions and metadata; public versions omit those comments.

## Design boundaries

`shikumi-devdoc` is not intended to become a general-purpose template engine.

- It does not provide a template language with conditionals or loops.
- Reference markers explicitly bring vocabulary or external-information values into a document.
- Semantic structure is validated through Shikumi regulations.
- Markdown realizers focus on converting a `SemanticView` into a concrete document format.
- Project-specific document sources and translation workflows remain in the consuming project.

These boundaries keep canonical sources, semantic information, realization rules, and published artifacts separate.

## License

`shikumi-devdoc` is released under the MIT License. See the top-level `LICENSE` file for details.
