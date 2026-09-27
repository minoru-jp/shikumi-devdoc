from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Vocabulary Reference Example", filename="vocabulary-reference.md", placeholders=False, heading="identity")
class DOCUMENT:
    # DOC-SNIPPET authoring-vocabulary-reference START
    class Overview:
        '''この文書の正本は {{TERM_001}} である。'''

        # DOC-SNIPPET authoring-code-field-snippet START
        merge @= TERMS.TERM_001
        # DOC-SNIPPET authoring-code-field-snippet END
    # DOC-SNIPPET authoring-vocabulary-reference END
