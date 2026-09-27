from shikumi_devdoc.norms.vocabulary import (
    alias,
    canonical,
    deprecated,
    glossary,
    replacement,
    term,
    title,
)


@canonical
@title("Example Glossary")
class VOCABULARY:
    """Public terms."""

    @term("Widget")
    class TERM_1:
        """The current public term."""
        glossary @= True
        alias @= "Component"
        alias @= "UI Widget"

    @term("OldWidget")
    class TERM_2:
        """The former public term."""
        glossary @= True
        deprecated @= True
        replacement @= "Widget"
