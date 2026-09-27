from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import glossary, preserve_spelling, vocabulary


@vocabulary
@canonical_source(
    "{{PROJECT.name}} Glossary",
    filename="GLOSSARY.md",
    placeholders=True,
    heading="identity",
)
class TERMS:
    """Terms used by {{PROJECT.name}}."""

    class TERM_1:
        """{{Widget}}

        A reusable widget.
        """

    class TERM_2:
        """{{InternalName}}

        An implementation-only identifier.
        """
        glossary @= False
        preserve_spelling @= True
