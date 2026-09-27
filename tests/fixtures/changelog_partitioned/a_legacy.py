from shikumi_devdoc.norms.changelog import ADDED, change, changelog_part, release, released_on


@changelog_part(order=20)
class CHANGELOG_PART:
    @release("1.0.0")
    class RELEASE_1:
        """First stable release."""
        released_on @= "2025-01-01"

        @change(ADDED)
        class CHANGE_1:
            """Added the original feature set."""
