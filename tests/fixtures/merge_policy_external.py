from shikumi_devdoc.norms.common import canonical_source


@canonical_source(
    "{{PROJECT.name}}",
    filename="external.md",
    merge_policy="external",
    heading="identity",
)
class DOCUMENT:
    """Version {{PROJECT.version}}."""
