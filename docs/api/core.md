# Core

Top-level public namespace.

## shikumi_devdoc

**Kind:** Namespace

A small entry namespace exposing Context APIs plus the standard-fields, authoring, and realization namespaces.

### Related

- [DIST_006](../specification/distribution.md#dist_006-small-top-level-public-namespace)

### Exports

It exports `Context`, `ContextError`, `UnknownContextKeyError`, `fields`, `norms`, and `realizers`. `fields`, `norms`, and `realizers` each expose an additional layer of namespaces grouped by purpose or semantic domain.
