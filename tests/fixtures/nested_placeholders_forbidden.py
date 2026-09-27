from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Snapshot", filename="snapshot.md", placeholders=False, heading="identity")
class SNAPSHOT:
    class Current:
        """Current version is {{PROJECT.version}}."""
