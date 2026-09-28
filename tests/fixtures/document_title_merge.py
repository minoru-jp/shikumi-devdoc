"""Canonical documents exercising templated node titles."""

from tests.fixtures.vocabulary_source import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source(
    "Title heading",
    filename="title-heading.md",
    merge_policy="all",
    heading="title",
)
class TITLE_HEADING:
    class SECTION_001:
        """Narrative node whose visible heading follows the templated title."""

        title @= "{{TERM_1}} for {{PROJECT.name}}"
        merge @= TERMS.TERM_1


@canonical_source(
    "Identity heading",
    filename="identity-heading.md",
    merge_policy="all",
    heading="identity",
)
class IDENTITY_HEADING:
    class SPEC_001:
        """Stable node whose human-readable title may change independently."""

        title @= "{{TERM_1}} for {{PROJECT.name}}"
        merge @= TERMS.TERM_1
