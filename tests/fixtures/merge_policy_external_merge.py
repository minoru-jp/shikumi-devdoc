from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source(
    "External",
    filename="external-merge.md",
    merge_policy="external",
    heading="identity",
)
class DOCUMENT:
    """No local reference is used."""

    merge @= ("unused", "Local")
