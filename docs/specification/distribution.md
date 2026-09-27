# Distribution

Rules for documentation assets included in the wheel and their status.

## DIST_001 Installed reference corpus

The wheel must include the complete `devdocs/` tree under `shikumi_devdoc/resources/devdocs/` as a reference corpus.

level: MUST

## DIST_002 Installed published documents

The wheel must include the published `README.md`, `STATUS.md`, `CHANGELOG.md`, and `docs/` under `shikumi_devdoc/resources/published_docs/`.

level: MUST

## DIST_003 Documentation resources are not public modules

Documentation resources included in the wheel must not be treated as importable `shikumi_devdoc` public API. They are package resources.

level: MUST NOT

## DIST_004 License distribution

The MIT License text must be distributed through project license metadata and need not be duplicated into published-document resources.

level: MUST

## DIST_005 Test dependency metadata

Project metadata must declare the test optional dependency on `pytest` so a test environment can be reconstructed from an sdist.

level: MUST

## DIST_006 Small top-level public namespace

The top-level `shikumi_devdoc` namespace must expose the Context APIs plus the `fields`, `norms`, and `realizers` namespaces and must not flatly re-export the authoring DSL or standard fields.

level: MUST

## DIST_007 Namespaced norms authoring surface

Public entities required for foundational canonical-source authoring must be grouped under `shikumi_devdoc.norms.<domain>`. Canonical-source metadata and shared policy belong in `shikumi_devdoc.norms.common`; canonical-document field writers and the validation system belong in `shikumi_devdoc.norms.document`. Optional standard field sets may be exposed under `shikumi_devdoc.fields.<domain>`, but they must not become mandatory semantics of the generic document core.

level: MUST

## DIST_008 Namespaced realizer surface

Standard realizers and public artifact values must be grouped under `shikumi_devdoc.realizers.<domain>`, where contextually sufficient short names such as `MarkdownRealizer` may be used within each domain.

level: MUST
