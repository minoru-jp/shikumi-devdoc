# Authoring Guide overview

This guide provides practical guidance for designing and maintaining canonical sources with `shikumi-devdoc`. The [Specification](../specification/INDEX.md) defines guaranteed behavior, and the [API Reference](../api/INDEX.md) describes the public interface. The Authoring Guide explains how to combine those mechanisms to write a document for a particular purpose.

The primary audience includes both humans and LLMs that design or update a repository's documentation system. For that reason, the guide is organized around the document you want to create rather than around framework feature categories.

## Do not create a prescribed document set

`shikumi-devdoc` does not require every repository to contain a README, Specification, API Reference, CHANGELOG, Glossary, or any other predefined set. Create only the documents the project needs. A small library may need only a README. A project with a strict public contract may also need a Specification or API Reference.

The documents described here are recommended authoring patterns for the generic canonical-document model, not mandatory document types. Do not create a document merely because it appears in this guide. Documents not listed here can also be authored with the same generic model.

## Start with the document you want to write

Choose the target document first, then use that page as the main working instructions.

- [Write a README](readme.md): create the repository entry point, overview, smallest useful example, and links to detailed docs.
- [Write a Getting Started guide](getting-started.md): guide a first-time user to one successful result.
- [Write a Configuration Guide](configuration-guide.md): explain configuration authoring, discovery, composition, and examples.
- [Write CLI documentation](cli-documentation.md): help command-line users find and perform operations.
- [Write a Specification](specification.md): structure normative contracts that implementation and compatibility must follow.
- [Write an API Reference](api-reference.md): record public API names, kinds, inputs, outputs, details, and lifecycle information.
- [Write a CHANGELOG](changelog.md): record release-centered history.
- [Write a Glossary / Vocabulary](glossary.md): centralize concept names and definitions shared across documents.
- [Write Project Status](project-status.md): record current status, direction, and user-facing notices.
- [Build a document collection](collections.md): split a large body of documentation into independent documents by meaning.

Use [Advanced authoring](advanced-authoring.md) only when a cross-cutting design decision is needed. LLM-based workflows should also use [LLM workflow](llm-workflow.md) as an operating boundary.

## General principles

Design from the meaning that should be preserved in the canonical source, not from the appearance of the generated Markdown. Add structure only for a concrete reason such as validation, presentation, reuse, or centralized naming. Information with no clear structural benefit can remain ordinary prose.

A canonical document is reviewable output, but it is not the editing origin. Make changes in the canonical source or, where appropriate, realization context, then regenerate through validation and realization.

Do not treat more documents as inherently better. If an existing document already serves the purpose, do not create another one. Split documents only when their responsibilities are meaningfully independent.

## Each purpose page should be enough to begin

Each authoring pattern explains when to create the document, a recommended structure, the fields that are useful, examples, and designs to avoid. An author should be able to create the first canonical source from that page alone.

The Authoring Guide does not duplicate the full Specification or API Reference. Consult those when exact framework behavior is needed, but basic authoring should not require reading a chain of feature-specific guide pages first.
