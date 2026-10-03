# Writing a Specification

A Specification records contracts that implementation and compatibility are expected to follow, separately from narrative guides.

## When to create one

Create a Specification when implementations must agree on rules, compatibility depends on explicit contracts, or edge cases should not remain ambiguous. A small project whose contract is fully covered by its README or API surface does not need a separate Specification.

## Give each normative rule its own node

Do not place many independent normative rules in one large docstring. When a rule is worth changing, referencing, or relating independently, give it its own node. A Specification root should normally declare `heading="identity"`; use an opaque stable identity such as `SPEC_NNN` when stable identity is useful. The number is not a display order or visible section number. Put the human-readable rule title in `title @= ...`, so changing the title or a Vocabulary term does not change the stable heading fragment.

Use narrative `SECTION_NNN` containers for explanatory grouping when appropriate.

## Use the standard field set

`shikumi_devdoc.fields.specification` provides `level`, `condition`, `detail`, `related`, and the values `MUST`, `MUST_NOT`, `SHOULD`, `SHOULD_NOT`, `MAY`, and `INFORMATIVE`. Use only the fields the rule needs. Human-readable node titles use `shikumi_devdoc.norms.document.title`.

```python
from shikumi_devdoc.fields.specification import MUST, condition, level
from shikumi_devdoc.norms.document import title


class SPEC_001:
    """The implementation returns an error when the input is invalid."""

    title @= "Invalid input"
    level @= MUST
    condition @= "The input fails validation."
```

## Use `related` as a dependency direction

Treat `related` as a directed semantic dependency rather than a symmetric "see also" link. Reference from the dependent rule toward the more foundational rule. Do not duplicate reverse backlinks in the canonical source.

If Python imports become cyclic, reconsider the documentation structure before introducing a mechanism to bypass the cycle. Ask whether a shared rule belongs in a more foundational document, or whether the reverse relation is merely an association rather than a dependency. Prefer specification structures that avoid cyclic dependencies. A nested `related` target must belong to a canonical document that uses `heading="identity"`; the validator rejects nested targets under `heading="title"`. A document root itself remains referenceable by filename without a fragment.

Keep Python object relations in `related`; do not encode Markdown filenames or `#fragments` in canonical source. The Markdown realizer derives source and target canonical document logical paths from canonical-source provenance plus each declared filename, relativizes those paths, and combines the result with the logical fragment computed from the target heading it actually emits. This logical path describes canonical-document topology, not the realization output directory. The fragment convention is GitHub-compatible rather than guaranteed by Markdown itself. If publication preserves that topology and compatible heading slugs, links normally remain valid as generated; otherwise rewrite the realized Markdown links during translation or publication rather than changing canonical `related` values to match published URLs.

## Split by semantic domain when the Specification grows

When areas such as paths, configuration, output, and CLI contracts can be changed and referenced independently, split the Specification into a document collection. Keep each document independently validatable and realizable.
