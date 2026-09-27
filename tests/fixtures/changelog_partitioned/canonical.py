from shikumi_devdoc.norms.changelog import ADDED, canonical, change, changelog, release, unreleased


@canonical
@changelog("Partitioned Changelog")
class CHANGELOG:
    """Release history split across physical modules."""

    @release()
    class RELEASE_1:
        """Changes planned for the next release."""
        unreleased @= True

        @change(ADDED)
        class CHANGE_1:
            """Added the partitioning example."""
