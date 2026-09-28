from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import prose_field
from tests.fixtures.vocabulary_collision_a import VocabularyA

term_field = prose_field("local term")


@canonical_source("Ambiguous field reference", filename="ambiguous-field.md", merge_policy="local", heading="identity")
class AMBIGUOUS_FIELD_REFERENCE:
    """{{TERM_001}}"""

    TERM_001 = term_field
    TERM_001 @= "Local term"
    merge @= VocabularyA.TERM_001
