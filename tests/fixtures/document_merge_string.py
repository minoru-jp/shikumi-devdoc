from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source(
    "Merge", filename="merge-string.md", merge_policy="local", heading="identity"
)
class DOCUMENT:
    """{{value}}"""

    merge @= ("value", "Local {{external}}")
