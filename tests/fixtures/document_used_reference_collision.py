from shikumi_devdoc.norms.common import canonical_source, merge


@canonical_source("Used collision", filename="used-collision.md", merge_policy="local", heading="identity")
class USED_COLLISION:
    """{{same}}"""

    merge @= ("same", "A")
    merge @= ("same", "B")
