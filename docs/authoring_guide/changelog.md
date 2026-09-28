# Writing a CHANGELOG

A CHANGELOG is release-centered historical record. Facts about past releases should remain stable when the document is regenerated later.

## When to create one

Create a CHANGELOG when users need to inspect release differences, breaking changes, fixes, or migration-relevant history. It is not mandatory for projects whose internal development notes are sufficient.

## Make each release a node

Use a node per release and select the needed fields from `shikumi_devdoc.fields.changelog`: `version`, `released_on`, `added`, `changed`, `deprecated`, `removed`, `fixed`, and `security`.

```python
from shikumi_devdoc.fields.changelog import added, fixed, version

class V1_2_0:
    """Release 1.2.0."""

    version @= "1.2.0"
    added @= "Added the public `run()` operation."
    fixed @= "Fixed configuration-path resolution."
```

Change-category fields are literal list content. Do not write `{{...}}` inside them expecting template expansion. Write the historical wording that should remain fixed.

## Separate current context from historical facts

The current project version may come from realization context, but past release versions and their changes belong directly in the canonical source. Re-realizing the document must not rewrite old CHANGELOG entries with current values. Set the CHANGELOG canonical source to `merge_policy="forbidden"` so both local and external merge are rejected.

## Subject lifecycle can also live with the subject

If an API or configuration item should reveal its own introduction, deprecation, removal, replacement, or migration path, use lifecycle fields on that subject as well.

```python
introduced @= "0.2.0"
deprecated @= "0.4.0"
replacement @= "new_api"
migration @= "Replace `old_api` with `new_api` when updating callers."
```
