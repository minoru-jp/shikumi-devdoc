from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Vocabulary B", filename="B.md", merge_policy="local", heading="identity")
class VocabularyB:
    """Vocabulary B."""

    class TERM_001:
        """{{Beta}}

        Beta concept.
        """
