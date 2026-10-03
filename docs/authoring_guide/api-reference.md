# Writing an API Reference

An API Reference records the current public surface so readers can look up individual API subjects.

## When to create one

Create an API Reference for Python APIs, HTTP APIs, command objects, or other public surfaces where users need to inspect individual names, kinds, inputs, outputs, and details. It is a reference, not a tutorial.

## Make each API subject a node

Create a node for each API entry and put the visible API name in the `name` field. If API nodes will be cross-referenced, use `heading="identity"` on the canonical root. If keeping the class name synchronized with the public spelling would cause drift, use an opaque stable identity such as `API_NNN`. Split large packages or functional areas into a document collection when useful.

## Use the standard field set

`shikumi_devdoc.fields.api_reference` provides `name`, `kind`, `input`, `output`, `detail`, `related`, plus `NAMESPACE`, `TYPE`, `VALUE`, `OPERATION`, and `OTHER`.

```python
from shikumi_devdoc.fields.api_reference import OPERATION, input, kind, name, output


class API_001:
    """Process one request and return its result."""

    name @= "run"
    kind @= OPERATION
    input @= "request: Request"
    output @= "RunResult"
```

Use fields when inputs and outputs benefit from comparison, listing, or reuse. Background explanation and examples can remain prose.

## Keep lifecycle information beside the subject

When readers need to know when an API was introduced, deprecated, removed, replaced, or how to migrate, attach `introduced`, `deprecated`, `removed`, `replacement`, and `migration` from `shikumi_devdoc.fields.lifecycle` to the API node.

The CHANGELOG is release-centered. Lifecycle fields are subject-centered. It is valid for the same change event to appear in both because they answer different questions.
