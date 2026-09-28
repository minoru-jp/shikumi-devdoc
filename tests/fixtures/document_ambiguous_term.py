from tests.fixtures.vocabulary_collision_a import VocabularyA
from tests.fixtures.vocabulary_collision_b import VocabularyB
from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Ambiguous term", filename="ambiguous-term.md", merge_policy="local", heading="identity")
class DOCUMENT:
    """{{TERM_001}}."""

    merge @= VocabularyA.TERM_001
    merge @= VocabularyB.TERM_001
