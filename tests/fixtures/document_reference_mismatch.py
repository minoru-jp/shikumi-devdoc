from tests.fixtures.vocabulary_source import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source("Merge scope", filename="document_reference_mismatch.md", merge_policy="local", heading="title")
class TITLE_1:
    """Root text uses {{widget}}."""

    merge @= ("widget", TERMS.TERM_1)

    class TITLE_2:
        """Local merges are not inherited: {{widget}}."""
        title @= "Child"
