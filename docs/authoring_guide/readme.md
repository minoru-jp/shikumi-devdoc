# Writing a README

A README is the repository entry point. Keep it focused on adoption decisions and the reader's next action.

## When to create a README

Create a README when a first-time reader needs to learn what the project does, how to install it, what to run first, and where to find details. Do not turn the README into the complete internal specification, configuration schema, or API catalog.

If a README is all the project needs, do not add other document patterns merely for completeness.

## Recommended structure

A useful default order is:

1. Briefly explain what the project does.
2. Put important usage or safety boundaries near the top.
3. Show installation.
4. Show the smallest useful example.
5. Link to detailed CLI, Configuration, API Reference, or Specification documents that actually exist.

If a long tutorial or complete reference is needed, split it into a Getting Started guide or a dedicated reference instead of continually expanding the README.

## Keep the canonical source prose-oriented

A README is usually a narrative document, so docstring prose and nested document nodes are normally enough. Record each node's human-readable title with `title @= ...`, keep it separate from class identity, and select `heading="title"` on the canonical root so resolved titles become Markdown headings.

Use `test_target_field` only when ordinary tests should inspect the exact code example to protect it against implementation drift. Small illustrative snippets may stay directly in the docstring, and Markdown fences belong in the surrounding template. Put values such as the current project version in realization context only when they are expected to change on re-realization.

## Minimal example

```python
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source("Example", filename="README.md", merge_policy="local", heading="title")
class README:
    """A small tool for processing example inputs."""

    class SECTION_001:
        """Install the package with your normal Python package workflow."""
        title @= "Installation"

    class SECTION_002:
        """Run the smallest useful example, then link to detailed guides."""
        title @= "Quick start"
```

There is no README-specific schema. This is just one composition of the generic canonical-document model. Add only the sections the repository needs.

## Avoid

Do not duplicate every CLI option, configuration rule, or normative requirement in the README. Let the README provide orientation and links while the detailed source of truth remains in the document designed for that purpose.

Do not force the class name to track the visible heading text. When that creates drift, use an opaque identity such as `SECTION_NNN`.
