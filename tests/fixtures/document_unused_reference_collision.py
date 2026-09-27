from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Unused collision", filename="unused-collision.md", placeholders=False, heading="identity")
class UNUSED_COLLISION:
    """No ambiguous reference is used."""

    merge @= ("same", "A")
    merge @= ("same", "B")
