from tests.fixtures import vocabulary_terms as terms
from shikumi_devdoc.norms.changelog import ADDED, canonical, change, changelog, release, released_on, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@changelog("{{PROJECT.name}} Changelog")
class CHANGELOG:
    """Release history for {{PROJECT.name}}."""

    @release("{{PROJECT.version}}")
    class RELEASE_1:
        """First public release."""
        released_on @= "2026-09-13"

        @change(ADDED)
        class CHANGE_1:
            """Added {{TERM_1}} support."""
            vocabulary_refs @= (terms.TERM_1,)
