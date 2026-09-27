from shikumi_devdoc.norms.changelog import ADDED, change, changelog_part, release, unreleased


@changelog_part(order=10)
class CHANGELOG_PART:
    @release()
    class RELEASE_1:
        """Second unreleased section."""
        unreleased @= True

        @change(ADDED)
        class CHANGE_1:
            """Second pending change."""

    @release("1.0.0")
    class RELEASE_2:
        """Duplicate release label source B."""

        @change(ADDED)
        class CHANGE_1:
            """Second historical change."""
