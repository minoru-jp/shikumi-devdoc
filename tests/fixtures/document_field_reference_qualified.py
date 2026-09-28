from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import prose_field
from tests.fixtures.vocabulary_collision_a import VocabularyA

term_field = prose_field("local term")


@canonical_source("Qualified field reference", filename="qualified-field.md", merge_policy="local", heading="identity")
class QUALIFIED_FIELD_REFERENCE:
    """{{local_term}} and {{VocabularyA.TERM_001}}."""

    TERM_001 = term_field
    TERM_001 @= "Local term"
    merge @= ("local_term", TERM_001)
    merge @= VocabularyA.TERM_001
