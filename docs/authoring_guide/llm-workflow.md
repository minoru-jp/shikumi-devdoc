# LLM authoring workflow

An LLM should identify the purpose of the document first and use the matching authoring pattern as the primary instruction set.

## Decide which documents are actually needed

Do not create a README, Specification, API Reference, CHANGELOG, and Glossary as a default bundle merely because the repository was inspected. Determine what users need, what public surface exists, and what contracts require maintenance, then create only the necessary documents.

For new documentation, start from the [Authoring Guide overview](overview.md) and select the purpose-specific page. For an existing repository, first read the current documentation architecture and canonical-source boundaries and preserve established responsibilities unless there is a clear reason to redesign them.

## Use the purpose page as the main instructions

When writing a Specification, start with the Specification page. When writing an API Reference, start with the API Reference page. Do not begin by reading every feature-specific concept and inventing a composition from scratch.

Consult the Specification or API Reference only when exact framework behavior is unclear, and use Advanced authoring only for cross-cutting decisions that the purpose page does not settle.

## Edit canonical sources, not generated documents

Do not patch canonical documents or published Markdown locally as the source of truth. Return changes to the corresponding canonical source, Vocabulary, or realization context, run validation and realization, and review the regenerated differences.

## Avoid over-structuring

LLMs tend to turn every discovered rule into a field, Vocabulary term, or separate document. Require a concrete benefit such as validation, reuse, stable identity, presentation, or testability before adding structure. Leave ordinary prose as prose.

Likewise, do not treat more files as an improvement by itself. Split into a collection only when reader goals and change responsibilities are meaningfully independent.
