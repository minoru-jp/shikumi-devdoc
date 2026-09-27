# Standard fields

Optional standard field sets composed from generic field primitives. The generic document realizer does not special-case these definitions.

## fields

**Kind:** Namespace

Convenience namespace exposing standard fields, related constants, and helpers grouped by common document use.

name: shikumi_devdoc.fields

detail: Exports `shikumi_devdoc.fields.common`, `shikumi_devdoc.fields.specification`, `shikumi_devdoc.fields.api_reference`, `shikumi_devdoc.fields.changelog`, `shikumi_devdoc.fields.lifecycle`, and `shikumi_devdoc.fields.status`.

### common

**Kind:** Namespace

Shared field definitions used by multiple standard field sets.

name: shikumi_devdoc.fields.common

detail: Exports `shikumi_devdoc.fields.common.kind`, `shikumi_devdoc.fields.common.condition`, `shikumi_devdoc.fields.common.detail`, and `shikumi_devdoc.fields.common.related`. Node title belongs to `shikumi_devdoc.norms.document.title`.

### specification

**Kind:** Namespace

Standard fields and normative values commonly useful in specification-like documents. Their use is optional and adds no special semantics to the generic document core.

name: shikumi_devdoc.fields.specification

detail: Exports `shikumi_devdoc.fields.specification.level`, `shikumi_devdoc.fields.specification.condition`, `shikumi_devdoc.fields.specification.detail`, `shikumi_devdoc.fields.specification.related`, `shikumi_devdoc.fields.specification.MUST`, `shikumi_devdoc.fields.specification.MUST_NOT`, `shikumi_devdoc.fields.specification.SHOULD`, `shikumi_devdoc.fields.specification.SHOULD_NOT`, `shikumi_devdoc.fields.specification.MAY`, and `shikumi_devdoc.fields.specification.INFORMATIVE`. Node title belongs to `shikumi_devdoc.norms.document.title`.

### api_reference

**Kind:** Namespace

Standard fields and API-kind values commonly useful in API-reference-like documents.

name: shikumi_devdoc.fields.api_reference

detail: Exports `shikumi_devdoc.fields.api_reference.name`, `shikumi_devdoc.fields.api_reference.kind`, `shikumi_devdoc.fields.api_reference.input`, `shikumi_devdoc.fields.api_reference.output`, `shikumi_devdoc.fields.api_reference.detail`, `shikumi_devdoc.fields.api_reference.related`, `shikumi_devdoc.fields.api_reference.NAMESPACE`, `shikumi_devdoc.fields.api_reference.TYPE`, `shikumi_devdoc.fields.api_reference.VALUE`, `shikumi_devdoc.fields.api_reference.OPERATION`, `shikumi_devdoc.fields.api_reference.OTHER`, `shikumi_devdoc.fields.api_reference.API_NAMESPACE`, `shikumi_devdoc.fields.api_reference.API_TYPE`, `shikumi_devdoc.fields.api_reference.API_VALUE`, `shikumi_devdoc.fields.api_reference.API_OPERATION`, and `shikumi_devdoc.fields.api_reference.API_OTHER`.

### changelog

**Kind:** Namespace

Standard release metadata fields and change-category list fields commonly useful in changelog-like documents.

name: shikumi_devdoc.fields.changelog

detail: Exports `shikumi_devdoc.fields.changelog.version`, `shikumi_devdoc.fields.changelog.released_on`, `shikumi_devdoc.fields.changelog.added`, `shikumi_devdoc.fields.changelog.changed`, `shikumi_devdoc.fields.changelog.deprecated`, `shikumi_devdoc.fields.changelog.removed`, `shikumi_devdoc.fields.changelog.fixed`, and `shikumi_devdoc.fields.changelog.security`.

### lifecycle

**Kind:** Namespace

Standard fields for recording introduction, deprecation, removal, replacement, and migration information on documented subjects.

name: shikumi_devdoc.fields.lifecycle

detail: Exports `shikumi_devdoc.fields.lifecycle.introduced`, `shikumi_devdoc.fields.lifecycle.deprecated`, `shikumi_devdoc.fields.lifecycle.removed`, `shikumi_devdoc.fields.lifecycle.replacement`, and `shikumi_devdoc.fields.lifecycle.migration`.

### status

**Kind:** Namespace

Standard fields and notice-kind values commonly useful in project-status-like documents.

name: shikumi_devdoc.fields.status

detail: Exports `shikumi_devdoc.fields.status.kind`, `shikumi_devdoc.fields.status.condition`, `shikumi_devdoc.fields.status.related`, and `shikumi_devdoc.fields.status.GENERAL`. Node title belongs to `shikumi_devdoc.norms.document.title`.

### design_contract

**Kind:** Value

The standard field sets are predefined combinations of generic field primitives and do not add dedicated validators or realizer dispatch.

name: standard field-set contract
