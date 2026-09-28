from shikumi_devdoc.norms.common import canonical_source, summary


@summary('Usage guidance for the package.')
@canonical_source("Guide", filename="guide.md", order=10, merge_policy="local", heading="identity")
class GUIDE:
    """Guide document."""
