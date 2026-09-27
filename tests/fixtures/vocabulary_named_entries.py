from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import glossary, vocabulary


@vocabulary
@canonical_source("Named entries", filename="GLOSSARY.md", heading="identity")
class TERMS:
    """Vocabulary entries need no TERM_N naming convention."""

    class Widget:
        """{{Widget}}

        A named vocabulary entry.
        """
        glossary @= True
