from tests.fixtures import vocabulary_terms as terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("Repeated reference")
class TITLE_1:
    """{{TERM_1}} appears twice: {{TERM_1}}."""

    vocabulary_refs @= (terms.TERM_1,)
