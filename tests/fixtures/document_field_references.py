from shikumi_devdoc.norms.common import APPEND, canonical_source
from shikumi_devdoc.norms.document import list_field, prose_field

shared = list_field("shared", str)
first = shared
second = shared
summary = prose_field("summary")


@canonical_source(
    "Field references",
    filename="field-references.md",
    merge_policy="local",
    unreferenced_fields=APPEND,
    heading="identity",
)
class FIELD_REFERENCES:
    """{{summary}}"""

    first @= "A"
    second @= "B"
    summary @= "First:\n{{first}}\n\nSecond:\n{{second}}"
