from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Multiple declarations", filename="GLOSSARY.md", heading="identity")
class TERMS:
    """Invalid multiple declaration example."""

    class BROKEN:
        """
        {{First}}{{Second}}

        Two declaration markers cannot occupy the declaration line.
        """
