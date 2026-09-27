# Writing a Configuration Guide

A Configuration Guide helps users understand how to author and reason about configuration.

## When to create one

Create one when the project exposes configuration files, a declarative schema, multiple sources, composition, or other behavior that cannot be used safely from a small README fragment alone. If configuration consists of only a few simple values, a README or API Reference may be enough.

## Organize around user decisions

Explain not only syntax, but where configuration lives, how it is discovered, how it is selected and combined, and what it affects. When the guide grows, split it by meaningful concerns such as discovery, schema/reference, selection, composition, output, and examples.

## Separate only test-target configuration examples

Use `test_target_field` for TOML, YAML, JSON, or similar examples only when parsing or schema validation should inspect the exact field value. Small illustrative examples may stay directly in docstring fenced blocks.

```toml
[tool.example]
enabled = true
```

`test_target_field` does not add Markdown fences and does not guarantee that an example has been tested. Put the fence in the docstring and exercise the corresponding parser or project configuration loader from the regular test suite.

## Separate guide material from the Specification

The guide explains how to configure the project. Exact precedence, collision behavior, path resolution, forbidden combinations, and other compatibility contracts belong in a Specification when the project has one. Link to the relevant specification document instead of copying the full rule text.
