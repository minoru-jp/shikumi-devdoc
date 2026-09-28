from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import field

version = field("version")
note = field("note")


@canonical_source("Snapshot", filename="snapshot.md", merge_policy="forbidden", heading="identity")
class DOCUMENT:
    """Historical snapshot."""

    version @= "1.2.3"
    note @= "Literal {{PROJECT.version}}"
