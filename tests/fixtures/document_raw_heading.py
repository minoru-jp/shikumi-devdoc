from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source("Raw heading", filename="document_raw_heading.md", merge_policy="all", heading="identity")
class TITLE_1:
    """## This heading bypasses the semantic structure."""
