from shikumi_devdoc.norms.changelog import CHANGED, change, changelog_part, release, released_on


@changelog_part(order=10)
class CHANGELOG_PART:
    @release("2.0.0")
    class RELEASE_1:
        """Second major release."""
        released_on @= "2026-01-01"

        @change(CHANGED)
        class CHANGE_1:
            """Changed the public behavior."""
