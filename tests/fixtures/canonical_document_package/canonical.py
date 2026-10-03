from shikumi_devdoc.norms.common import canonical_source


@canonical_source(
    "Fixture", filename="fixture.md", merge_policy="local", heading="identity"
)
class DOCUMENT:
    class Entry:
        pass
