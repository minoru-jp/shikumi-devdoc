from shikumi_devdoc.norms.common import canonical_source


@canonical_source(
    "Snapshot", filename="snapshot.md", merge_policy="local", heading="identity"
)
class SNAPSHOT:
    """Current version is {{PROJECT.version}}."""
