from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source(
    "{{PROJECT.name}}", filename="all.md", merge_policy="all", heading="identity"
)
class DOCUMENT:
    """{{local}} {{PROJECT.version}}"""

    merge @= ("local", "Local")
