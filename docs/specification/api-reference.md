# Domain field vocabularies

Rules for composing domain-specific documentation such as Specification and API Reference from author-defined or standard field sets.

## APIREF_001

The generic document core must not define domain keywords such as API kinds or normative levels as mandatory semantics. Even when standard field sets provide convenience values, authors must be able to replace them with custom fields and values.

title: Domain keywords belong to authors

level: MUST

## APIREF_002

Information such as API inputs and outputs may be described as values of author-defined fields.

title: Inputs and outputs as fields

level: MAY

## APIREF_003

Domain-specific supplemental information must be expressible with ordinary fields, prose fields, or document-node hierarchy without requiring a dedicated realizer.

title: Generic domain details

level: MUST

## APIREF_004

A domain document must be an ordinary `@canonical_source(..., filename=...)` document and must not require dedicated root/part concepts.

title: Ordinary canonical documents

level: MUST

## APIREF_005

The author must determine heading order and hierarchy through nested-class placement. The realizer must not reconstruct hierarchy from domain kinds.

title: Author-owned document hierarchy

level: MUST

## APIREF_006

A domain that needs relationship information may use the standard `related` field, whose semantic references realize as logical Markdown links; define its own relation field with `reference_field(...)`; or retain literal relationship metadata with `field(...)`. The generic document core does not define relationship direction or domain meaning.

title: Relations as field vocabulary

level: MAY

## APIREF_007

A domain-specific realizer must not be required. The generic document Markdown realizer must be sufficient to realize canonical documents without losing the described information.

title: Generic realization is sufficient

level: MUST

## APIREF_008

A collection index may be derived by the index realizer from a canonical-source package rather than being duplicated as a dedicated canonical source.

title: Collection index is derived from the package

level: MUST

## APIREF_009

Domain identities such as API identity may be represented by class nesting or author-defined fields, but the foundation must not own that domain meaning.

title: Domain identity is author-owned

level: MUST

## APIREF_010

When a public name differs from a Python identifier, a domain may retain it with a field such as `name = field("name", str)`.

title: Explicit display names

level: MAY

## APIREF_011

Class nesting denotes document hierarchy. Whether a domain also assigns meaning such as API ownership to that nesting is owned by the domain-field-vocabulary author.

title: Nesting semantics remain author-owned

level: MUST

## APIREF_012

The foundation must not introduce a dedicated root entity solely to collect multiple domain documents.

title: No domain collection root

level: MUST

## APIREF_013

The standard field sets under `shikumi_devdoc.fields` may be provided as predefined combinations of generic field primitives, but they must not introduce dedicated validators, dedicated realizer dispatch, or mandatory domain rules.

title: Standard fields are conveniences

level: MUST
