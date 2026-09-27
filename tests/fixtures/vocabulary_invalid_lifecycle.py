from shikumi_devdoc.norms.vocabulary import (
    alias,
    canonical,
    deprecated,
    replacement,
    term,
    title,
)


@canonical
@title("Invalid Glossary")
class VOCABULARY:
    """Invalid relationships."""

    @term("Widget")
    class TERM_1:
        """Current term."""
        alias @= "OldWidget"

    @term("OldWidget")
    class TERM_2:
        """Old term."""
        deprecated @= True
        replacement @= "Missing"
