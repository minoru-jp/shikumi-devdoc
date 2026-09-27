from tests.fixtures import vocabulary_terms as terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("{{PROJECT.name}}")
class TITLE_1:
    """Version {{PROJECT.version}} documents the {{TERM_1}} API."""

    vocabulary_refs @= (terms.TERM_1,)

    @title("Install")
    class TITLE_2:
        """Requires Python {{PYTHON.minimum}}+."""
