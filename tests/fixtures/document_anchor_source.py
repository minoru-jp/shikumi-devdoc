from shikumi_devdoc.norms.document import anchor, canonical, title


@canonical
@title("Guide")
class TITLE_1:
    r"""Start with {{#install}}. Write `\{{#literal}}` to show the marker literally."""

    anchor @= "guide"

    @title("Install [Linux]")
    class TITLE_2:
        """Installation instructions."""

        anchor @= "install"
