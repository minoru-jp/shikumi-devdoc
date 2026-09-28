from shikumi_devdoc.norms.common import APPEND, IGNORE, canonical_source, merge
from shikumi_devdoc.norms.document import (
    test_target_field,
    field,
    list_field,
    prose_field,
    table_field,
)

status_writer = field("status", str)
status_value = status_writer
changes = list_field("changes", str)
example = test_target_field("example")
compatibility = table_field("compatibility", columns=("runtime", "status"))
summary = prose_field("summary")
hidden = field("hidden", str)


@canonical_source(
    "Field templates",
    filename="field-templates.md",
    order=10,
    merge_policy="all",
    unreferenced_fields=APPEND,
    heading="identity",
)
class FIELD_TEMPLATES:
    r"""{{summary}}

External value: {{PROJECT.name}}.
"""

    status_value @= "stable {{PROJECT.name}}"
    summary @= r"Status: {{status}}. Literal marker: \{{changes}}."
    changes @= "Added {{PROJECT.name}} support."
    changes @= "Kept literal {{status}} syntax."
    example @= 'print("{{PROJECT.name}}")'
    compatibility @= ("{{PROJECT.name}} runtime", "supported")

    merge @= ("summary", summary)
    merge @= ("status", status_value)


@canonical_source(
    "Ignored fields",
    filename="ignored-fields.md",
    order=20,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="identity",
)
class IGNORED_FIELDS:
    """Only {{summary}} is rendered."""

    summary @= "Visible prose."
    hidden @= "source-only metadata"
    merge @= ("summary", summary)
