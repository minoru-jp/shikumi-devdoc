from tests.fixtures.vocabulary_source import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Literal placeholders", filename="document_literal_placeholders.md", merge_policy="local", heading="identity")
class TITLE_1:
    r"""GitHub Actions keeps `${{ matrix.os }}`.

    An escaped marker stays literal: `\{{widget}}`.
    A semantic marker still resolves to {{internal_name}}.
    """

    merge @= ("internal_name", TERMS.TERM_2)
