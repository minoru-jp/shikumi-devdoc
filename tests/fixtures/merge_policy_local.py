from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source(
    "Local", filename="local.md", merge_policy="local", heading="identity"
)
class DOCUMENT:
    """{{local}} {{PROJECT.version}}"""

    merge @= ("local", "Local")
