from shikumi_devdoc.norms.changelog import (
    ADDED,
    canonical,
    change,
    changelog,
    release,
    released_on,
    unreleased,
)


@canonical
@changelog("Invalid Changelog")
class CHANGELOG:
    """Invalid release ordering."""

    @release("1.0.0")
    class RELEASE_1:
        """Released."""
        released_on @= "2026-09-13"

        @change(ADDED)
        class CHANGE_1:
            """Added something."""

    @release()
    class RELEASE_2:
        """Should have been first and must not have a date."""
        unreleased @= True
        released_on @= "2026-09-14"

        @change(ADDED)
        class CHANGE_1:
            """Added something else."""
