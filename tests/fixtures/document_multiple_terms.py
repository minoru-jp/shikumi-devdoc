from shikumi_devdoc.norms.common import canonical_source, merge
from tests.fixtures.vocabulary_source import TERMS


@canonical_source(
    "Multiple vocabulary terms",
    filename="document_multiple_terms.md",
    merge_policy="local",
    heading="identity",
)
class TITLE_1:
    """{{widget}} uses {{internal_name}}."""

    merge @= ("widget", TERMS.TERM_1)
    merge @= ("internal_name", TERMS.TERM_2)
