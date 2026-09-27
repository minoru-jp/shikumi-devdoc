from tests.fixtures.vocabulary_collision_same_a import Vocabulary as VocabularyA
from tests.fixtures.vocabulary_collision_same_b import Vocabulary as VocabularyB
from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Module-qualified terms", filename="module-qualified-terms.md", placeholders=False, heading="identity")
class DOCUMENT:
    """{{vocabulary_collision_same_a.Vocabulary.TERM_001}} and {{vocabulary_collision_same_b.Vocabulary.TERM_001}}."""

    merge @= VocabularyA.TERM_001
    merge @= VocabularyB.TERM_001
