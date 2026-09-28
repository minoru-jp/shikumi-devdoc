from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Vocabulary A", filename="A.md", merge_policy="local", heading="identity")
class VocabularyA:
    """Vocabulary A."""

    class TERM_001:
        """{{Alpha}}

        Alpha concept.
        """
