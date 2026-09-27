"""Target canonical document in a sibling logical package."""

from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Target", filename="target.md", placeholders=False, heading="identity")
class TARGET:
    class SPEC_001:
        """Target rule."""
