# Core

Rules shared across the documentation system.

## CORE_001 Canonical source

Every authoritative source unit that contributes to a canonical document must be marked with `@canonical_source`. Bare `@canonical_source` may also mark non-document canonical sources such as Vocabulary.

level: MUST

## CORE_002 Validate before realization

A semantic view passed to a standard realizer must have successfully validated against the corresponding regulation.

level: MUST

## CORE_003 Public documentation roles

README is the entry point; Project Status owns current state and future-facing notices; Specification owns current rules; API Reference owns public interfaces; CHANGELOG owns past changes. These roles do not require dedicated `shikumi-devdoc` document types and may be composed on the common document model.

level: INFORMATIVE

## CORE_004 Canonical document

A canonical document is the result of validating canonical source, injecting required realization context, and assembling a document with a realizer. `shikumi-devdoc` consistently owns artifacts through this canonical-document boundary.

level: INFORMATIVE

## CORE_005 Realization context

Realization context supplies values, such as the current version, that should not be frozen into canonical source. Context is not historical storage and is not a replacement for canonical source.

level: INFORMATIVE

## CORE_006 Published document boundary

A published document is a derivative made from a canonical document through translation, localization, prose adjustment, media conversion, distribution, or similar publication work. `shikumi-devdoc` does not prescribe a particular publication workflow.

level: INFORMATIVE

## CORE_007 Canonical source provenance

The provenance recorded by `@canonical_source` must be derived stably from Python module structure and must not depend on the process current working directory.

level: MUST

## CORE_008 Canonical document metadata

A canonical document's root title, filename, nested-heading policy, optional order, merge policy, and unreferenced-field policy must be declared as common metadata through `@canonical_source(...)`, independently from document-domain semantics. The author must explicitly select either `heading="title"` or `heading="identity"`; the realizer must not infer the policy from the document kind.

level: MUST

## CORE_009 Unified canonical document model

Canonical documents must use one document-node model. Root and nested classes share the same model, and a document is composed from docstring templates, author-defined fields, and nested class hierarchy.

level: MUST

## CORE_010 Merge policy

`@canonical_source(..., merge_policy=...)` must control which value sources template-bearing content may reference with four values: `"all"`, `"local"`, `"external"`, and `"forbidden"`. `"all"` allows both node-local references and external placeholders, `"local"` allows only node-local references, `"external"` allows only external placeholders, and `"forbidden"` allows neither. The default is `"all"`.

level: MUST

## CORE_010A Local merge prohibition

A canonical document using `merge_policy="external"` or `merge_policy="forbidden"` must not contain `merge @= ...` declarations, even when they are unused, and template-bearing content must not reference node-local bindings, including field bindings. Ordinary field values remain literal content, and placeholder-looking text inside them must not be interpreted as a template.

level: MUST

## CORE_010B Legacy placeholders compatibility

The deprecated `placeholders=True` parameter must be interpreted as `merge_policy="all"`, and `placeholders=False` as `merge_policy="local"`. `placeholders` and `merge_policy` must not be specified together. Direct API use of `placeholders` must emit a deprecation warning, CLI use must surface that warning, and `placeholders` is scheduled for removal in 1.0.0.

level: MUST

## CORE_011 Unreferenced field policy

`unreferenced_fields=APPEND` must realize fields not referenced by templates at the end of each document node. `unreferenced_fields=IGNORE` must retain such fields in canonical-source semantic information without emitting them into the canonical document.

level: MUST

## CORE_012 Canonical document logical path

A canonical document logical path must be derived deterministically from the parent path of the Python-module provenance recorded by `CanonicalSource` together with the canonical filename declared by the document root. This logical path describes the canonical document's provenance and relative topology within the canonical-document system; it must not represent the realization output directory or the published-document location.

level: MUST
