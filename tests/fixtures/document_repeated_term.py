from shikumi_devdoc.norms.common import canonical_source, merge
from tests.fixtures.vocabulary_source import TERMS


@canonical_source(
    "Repeated reference",
    filename="document_repeated_term.md",
    merge_policy="local",
    heading="identity",
)
class TITLE_1:
    """{{widget}} appears twice: {{widget}}."""

    merge @= ("widget", TERMS.TERM_1)
