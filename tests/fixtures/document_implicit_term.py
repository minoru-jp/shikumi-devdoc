from tests.fixtures.vocabulary_collision_a import VocabularyA
from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Implicit term", filename="implicit-term.md", merge_policy="local", heading="identity")
class DOCUMENT:
    """{{TERM_001}}."""

    merge @= VocabularyA.TERM_001
