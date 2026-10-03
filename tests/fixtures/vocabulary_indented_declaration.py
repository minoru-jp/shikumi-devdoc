from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Indented declaration", filename="GLOSSARY.md", heading="identity")
class TERMS:
    """Vocabulary declarations may follow normal Python docstring indentation."""

    class Widget:
        """
        {{Widget}}

        A named vocabulary entry.

            Relative indentation remains part of the definition.
        """
