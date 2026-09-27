from shikumi_devdoc.norms.document import anchor, canonical, title


@canonical
@title("Guide")
class TITLE_1:
    """Root."""

    anchor @= "same"

    @title("First")
    class TITLE_2:
        """First."""

        anchor @= "same"

    @title("Second")
    class TITLE_3:
        """Second."""

        anchor @= "not allowed"
