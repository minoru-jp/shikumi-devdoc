from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import alias, deprecated, replacement, vocabulary


@vocabulary
@canonical_source("Invalid Glossary", filename="GLOSSARY.md", heading="identity")
class TERMS:
    """Invalid lifecycle examples."""

    class TERM_1:
        """{{Widget}}

        Current term.
        """

        alias @= "OldWidget"

    class TERM_2:
        """{{OldWidget}}

        Old term.
        """

        deprecated @= True
        replacement @= "MissingWidget"
