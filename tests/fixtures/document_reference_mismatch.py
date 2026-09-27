from tests.fixtures import vocabulary_terms as terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("Reference validation")
class TITLE_1:
    """Root text does not use a vocabulary term."""

    # This reference is intentionally misplaced: child references are local.
    vocabulary_refs @= (terms.TERM_1,)

    @title("Child")
    class TITLE_2:
        """This child uses {{TERM_1}} without declaring a local reference."""
