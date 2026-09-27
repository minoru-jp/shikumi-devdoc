from tests.fixtures import vocabulary_terms as terms
from shikumi_devdoc.norms.changelog import ADDED, canonical, change, changelog, release, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@changelog("Reference validation")
class CHANGELOG:
    """No vocabulary term is used by the root."""

    @release("0.1.0")
    class RELEASE_1:
        """Release notes without a term."""

        @change(ADDED)
        class CHANGE_1:
            """Added {{TERM_1}} support."""
            # Intentionally missing vocabulary_refs.
