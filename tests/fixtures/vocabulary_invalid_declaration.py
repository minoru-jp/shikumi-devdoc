from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Invalid declaration", filename="GLOSSARY.md", heading="identity")
class TERMS:
    """Invalid term declaration examples."""

    class BROKEN:
        """
        Introductory prose may not precede the declaration.

        {{Broken}}

        This marker is ordinary prose because it is not at the normalized start.
        """
