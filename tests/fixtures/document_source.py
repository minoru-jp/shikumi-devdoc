from tests.fixtures.vocabulary_source import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source("{{PROJECT.name}}", filename="document_source.md", merge_policy="all", heading="title")
class TITLE_1:
    """Version {{PROJECT.version}} documents the {{widget}} API.

    Translation-sensitive identifier: {{internal_name}}.
    """

    merge @= ("widget", TERMS.TERM_1)
    merge @= ("internal_name", TERMS.TERM_2)

    class TITLE_2:
        """Requires Python {{PYTHON.minimum}}+."""
        title @= "Install"
