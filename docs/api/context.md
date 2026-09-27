# Context

Top-level public APIs for holding and resolving external context.

## shikumi_devdoc.Context

**Kind:** Type

A value object that holds JSON-compatible external information supplied at realization time and resolves values by dot-separated keys.

### Construction

It can be constructed directly from a mapping, and `Context.from_json()` and `Context.from_mapping()` are also available.

### shikumi_devdoc.Context.from_json

**Kind:** Operation

Construct a Context from a JSON object string.

#### Inputs

##### text

**Type:** `str`

A string representing a JSON object.

#### Outputs

##### Output

**Type:** `Context`

The normalized Context.

### shikumi_devdoc.Context.resolve

**Kind:** Operation

Resolve a dot-separated key and return a string representation suitable for embedding in Markdown.

#### Inputs

##### key

**Type:** `str`

For example, `project.version`.

#### Outputs

##### Output

**Type:** `str`

The resolved value as text.

## shikumi_devdoc.ContextError

**Kind:** Type

Base error for Context construction or resolution failures.

## shikumi_devdoc.UnknownContextKeyError

**Kind:** Type

Error indicating an attempt to resolve a context key that does not exist.
