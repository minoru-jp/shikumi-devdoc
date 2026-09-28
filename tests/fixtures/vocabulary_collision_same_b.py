from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Same-name Vocabulary B", filename="same-b.md", merge_policy="local", heading="identity")
class Vocabulary:
    """Vocabulary B with a shared Python container name."""

    class TERM_001:
        """{{Delta}}

        Delta concept.
        """
