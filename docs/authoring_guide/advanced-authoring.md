# Advanced authoring decisions

Use the purpose-specific authoring patterns first. Read this page only when a cross-cutting design decision remains.

## Separate prose from fields

Put background, rationale, and explanatory flow in prose. Move information into fields only when comparison, enumeration, reuse, validation, or a particular presentation provides a concrete benefit.

Do not turn everything that could be structured into a field. Use `field`, `list_field`, `table_field`, `prose_field`, and `reference_field` when the separated information structure is useful. Use `test_target_field` for literal text that ordinary tests should inspect directly, not as a presentation primitive.

## Separate node identity from display title

A nested node's human-readable title is always recorded with `title @= "..."`; `@title(...)` is not a separate title syntax. Title text can resolve same-node `merge` references and realization context.

For narrative documents, select `@canonical_source(..., heading="title")` so the resolved title becomes the Markdown heading. When the node does not need a meaningful external name, an opaque stable identity such as `SECTION_NNN` is recommended. The number is not display order, heading depth, or a published section number. Preserve the identity across reordering, title changes, and hierarchy moves.

```python
@canonical_source("Guide", filename="guide.md", merge_policy="local", heading="title")
class GUIDE:
    class SECTION_017:
        """Introductory text."""

        title @= "Getting started"
```

When nested nodes need to be stable semantic reference targets, select `heading="identity"`. In that mode the identity remains the Markdown heading and `title` is realized as human-readable metadata. `heading="title"` nested nodes are intentionally not valid `related` targets because title, Vocabulary, or context changes could change their fragments.

The choice of identity naming scheme is an authoring convention rather than a validator requirement; purpose-specific schemes such as `SPEC_NNN` are valid. The requirement that a nested reference target belong to an `identity`-heading document is validated.

## Indent docstrings naturally

Canonical-root and document-node docstrings are normalized with behavior equivalent to `inspect.cleandoc()` before they become semantic content. Indent them naturally within Python scope. Common indentation is removed while relative indentation inside the body is preserved.

Raw vs non-raw strings and triple single vs double quotes remain author choices.

```python
class SECTION_001:
    """
    Introductory text.

        Relative indentation is preserved.
    """
```

## Keep local references local to the node

A field binding such as `name @= value` is available from the same node's template as `{{name}}`. Use `merge @= target` for class targets such as Vocabulary terms, or `merge @= ("name", target)` when an explicit alias is needed.

Do not use merge as a general macro system for fragmenting long prose. Docstrings, `prose_field`, and `title @= ...` are template-bearing content. Ordinary scalar, list, table, and test target field values are literal content.

## Use realization context only for external values that may change

A value is a good realization-context candidate when it is allowed to change when the same canonical source is realized later. The current project version is a typical example. Historical release versions, accepted design decisions, and normative conditions should remain in the canonical source.

`merge_policy` does not constrain fields defined directly on the same node. It only constrains the explicit insertion channels provided by `merge @= ...` and external context. `"all"` allows both, `"local"` allows local merge only, `"external"` allows external context only, and `"forbidden"` rejects both. A value bound directly with `name @= value` remains referenceable from the node's templates under every policy, and the policy does not track where that Python value originated before assignment.

## Protect code examples with normal tests

Move sample code, configuration, commands, expected output, or similar fragments into `test_target_field` when ordinary tests should inspect the exact text. Put Markdown fences and language markers in the surrounding docstring, then verify the field value with pytest or another normal test mechanism. Do not make documentation generation execute code with `eval` or `exec` as a special testing DSL.

```python
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import test_target_field, title

example = test_target_field("example")

@canonical_source("Guide", filename="guide.md", merge_policy="local", heading="title")
class GUIDE:
    class SECTION_001:
        """
        ```python
        {{example}}
        ```
        """
        title @= "Example"
        example @= """
        print("hello")
        """
```

## Separate semantic references from publication links

Use `reference_field()` when a Python object relationship should remain navigable in published Markdown. The standard `related` field is a convenience field built on that presentation. Keep object relations in canonical source rather than writing Markdown filenames or fragments there.

The Markdown realizer derives each canonical document logical path from canonical-source provenance plus the declared canonical filename, relativizes the source and target logical paths, and combines that path with the logical fragment computed from the target heading it actually emits. It does not add explicit HTML anchors. These fragments use a GitHub-compatible heading-slug convention as a logical reference convention, not as a Markdown-standard guarantee. The realizer does not inspect, infer, or validate the eventual publication layout or downstream renderer behavior. If publication preserves the logical topology and compatible heading slugs, links normally remain valid as generated; otherwise rewrite the realized links during publication processing.
