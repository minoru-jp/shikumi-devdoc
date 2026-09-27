from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Merge", filename="merge-string.md", placeholders=False, heading="identity")
class DOCUMENT:
    """{{value}}"""

    merge @= ("value", "Local {{external}}")
