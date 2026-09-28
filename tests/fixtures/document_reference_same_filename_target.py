"""Reference target whose canonical filename collides with another document."""

from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Target", filename="collision.md", merge_policy="local", heading="identity")
class TARGET:
    class SPEC_001:
        """Target node."""


SPEC_001 = TARGET.SPEC_001
