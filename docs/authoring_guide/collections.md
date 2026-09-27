# Building a document collection

A collection is a set of canonical documents that can be read, changed, validated, and realized independently.

## When to create a collection

Do not split a document just because it is long. Split it when semantic areas have independent change responsibility, references, or reader goals. Specifications, API references, configuration guides, and CLI documentation often grow into collections.

Do not split small documents mechanically. If readers must consume every page in sequence for the content to make sense, one document may be the better representation.

## Make every document an independent canonical source

Do not invent a collection-wide document grammar. Give each page its own `@canonical_source(...)` root and keep it independently validatable and realizable.

```text
canonical_sources/
  specification/
    __init__.py
    overview.py
    paths.py
    output.py
```

## Keep order and summary as metadata

Use `@canonical_source(..., order=...)` only when the collection needs a stable human-facing order. Add `@summary(...)` when the index should explain the purpose of each document. Treat `order` as collection presentation metadata, not as document identity.

## Realize the index separately

Keep individual-document realization separate from collection-index realization. Do not rely on the document realizer to create `INDEX.md` implicitly. Use `render index` or `IndexMarkdownRealizer` for the package.

If the publication workflow translates the index, do not add prose to the published index that has no canonical source. Put that information in each document's `@summary(...)` instead.
