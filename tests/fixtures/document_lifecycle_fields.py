from shikumi_devdoc.fields.lifecycle import (
    deprecated,
    introduced,
    migration,
    removed,
    replacement,
)
from shikumi_devdoc.norms.common import APPEND, canonical_source


@canonical_source(
    "Lifecycle fields",
    filename="lifecycle-fields.md",
    placeholders=False,
    unreferenced_fields=APPEND,
    heading="identity",
)
class LIFECYCLE_FIELDS:
    """Lifecycle metadata remains ordinary author-defined document fields."""

    class OLD_API:
        """An API kept as a documentation tombstone after its lifecycle changed."""

        introduced @= "0.1.0"
        deprecated @= "0.3.0"
        removed @= "0.5.0"
        replacement @= "new_api"
        migration @= "Use `new_api` when migrating existing callers."
