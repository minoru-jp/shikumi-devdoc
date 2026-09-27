# Writing a Getting Started guide

A Getting Started guide is not a reference. It leads a first-time user through the shortest successful path.

## When to create one

Create a Getting Started guide when the README's smallest example is not enough to explain initial use. The goal is to lead the reader from prerequisites and installation to one successful result, not to cover every feature.

## Choose one happy path

Choose the most common path with the fewest dependencies. Present prerequisites, installation, minimal configuration, execution, and expected result in order. Avoid presenting many alternatives before the reader has completed the first successful flow. Link to alternatives afterward.

## Prefer executable examples

Move commands, Python snippets, or configuration fragments into `test_target_field` only when the normal test suite should inspect the exact text. Keep Markdown fences in the surrounding docstring and test the field value directly.

```bash
example --help
```

## Do not duplicate reference material

Explain only the settings and options needed for the walkthrough. Link to the Configuration Guide for the full configuration model, CLI documentation for the complete command surface, and the Specification for normative edge cases.
