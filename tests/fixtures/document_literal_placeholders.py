from tests.fixtures import vocabulary_terms as terms
from shikumi_devdoc.norms.document import canonical, title, vocabulary, vocabulary_refs


@canonical
@vocabulary(terms)
@title("Literal placeholders")
class TITLE_1:
    r"""GitHub Actions keeps `${{ matrix.os }}`.

    An escaped marker stays literal: `\{{TERM_1}}`.
    A semantic marker still resolves to {{TERM_2}}.
    """

    vocabulary_refs @= (terms.TERM_2,)
