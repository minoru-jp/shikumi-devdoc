from shikumi_devdoc.norms.vocabulary import canonical, glossary, preserve_spelling, term, title


@canonical
@title("{{PROJECT.name}} Glossary")
class VOCABULARY:
    """Terms used by {{PROJECT.name}}."""

    @term("Widget")
    class TERM_1:
        """A reusable widget."""
        glossary @= True

    @term("InternalName")
    class TERM_2:
        """An implementation-only identifier."""
        preserve_spelling @= True
