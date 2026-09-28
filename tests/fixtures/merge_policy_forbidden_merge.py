from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import system


@canonical_source(
    "Snapshot with merge",
    filename="snapshot-merge.md",
    merge_policy="forbidden",
    heading="identity",
)
class DOCUMENT:
    """Historical snapshot."""

    merge @= ("term", "unused")
