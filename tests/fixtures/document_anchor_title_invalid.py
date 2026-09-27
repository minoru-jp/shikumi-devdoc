from shikumi_devdoc.norms.document import anchor, canonical, title


@canonical
@title("{{#target}}")
class TITLE_1:
    """Root."""

    @title("Target")
    class TITLE_2:
        """Target body."""

        anchor @= "target"
