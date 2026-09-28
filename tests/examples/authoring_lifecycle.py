from shikumi_devdoc.fields.lifecycle import deprecated, introduced, migration, replacement
from shikumi_devdoc.norms.common import APPEND, canonical_source


@canonical_source(
    "Lifecycle example",
    filename="lifecycle-example.md",
    merge_policy="local",
    unreferenced_fields=APPEND,
    heading="identity",
)
class DOCUMENT:
    class OldApi:
        """Compatibility entry for an older API."""

        # DOC-SNIPPET authoring-lifecycle START
        introduced @= "0.2.0"
        deprecated @= "0.4.0"
        replacement @= "new_api"
        migration @= "Replace `old_api` with `new_api` when updating callers."
        # DOC-SNIPPET authoring-lifecycle END
