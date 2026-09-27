from shikumi_devdoc.norms.changelog import (
    ADDED,
    CHANGED,
    breaking,
    canonical,
    change,
    changelog,
    release,
    released_on,
    unreleased,
)


@canonical
@changelog("Example Changelog")
class CHANGELOG:
    """Release history."""

    @release()
    class RELEASE_1:
        """Work planned for the next release."""
        unreleased @= True

        @change(CHANGED)
        class CHANGE_1:
            """Changed the wire format."""
            breaking @= True

    @release("1.0.0")
    class RELEASE_2:
        """First stable release."""
        released_on @= "2026-09-13"

        @change(ADDED)
        class CHANGE_1:
            """Added the stable API."""
