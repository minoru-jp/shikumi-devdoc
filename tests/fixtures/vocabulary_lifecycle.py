from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import (
    alias,
    deprecated,
    replacement,
    vocabulary,
)


@vocabulary
@canonical_source("Example Glossary", filename="GLOSSARY.md", heading="identity")
class TERMS:
    """Public terms."""

    class TERM_1:
        """{{Widget}}

        The current public term.
        """
        alias @= "Component"
        alias @= "UI Widget"

    class TERM_2:
        """{{OldWidget}}

        The former public term.
        """
        deprecated @= True
        replacement @= "Widget"
