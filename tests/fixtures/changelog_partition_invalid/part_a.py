from shikumi_devdoc.norms.changelog import ADDED, change, changelog_part, release, unreleased


@changelog_part(order=10)
class CHANGELOG_PART:
    @release()
    class RELEASE_1:
        """First unreleased section."""
        unreleased @= True

        @change(ADDED)
        class CHANGE_1:
            """First pending change."""

    @release("1.0.0")
    class RELEASE_2:
        """Duplicate release label source A."""

        @change(ADDED)
        class CHANGE_1:
            """First historical change."""
