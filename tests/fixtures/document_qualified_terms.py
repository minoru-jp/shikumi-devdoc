from tests.fixtures.vocabulary_collision_a import VocabularyA
from tests.fixtures.vocabulary_collision_b import VocabularyB
from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Qualified terms", filename="qualified-terms.md", merge_policy="local", heading="identity")
class DOCUMENT:
    """{{VocabularyA.TERM_001}} and {{VocabularyB.TERM_001}}."""

    merge @= VocabularyA.TERM_001
    merge @= VocabularyB.TERM_001
