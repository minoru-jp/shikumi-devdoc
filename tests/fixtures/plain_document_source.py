from shikumi_devdoc.norms.common import canonical_source


@canonical_source(
    "{{PROJECT.name}}",
    filename="plain_document_source.md",
    merge_policy="all",
    heading="identity",
)
class TITLE_1:
    """Plain document."""
