"""Source canonical document referring to a sibling logical package."""

from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import canonical_source
from tests.fixtures.logical_reference_target.document import TARGET


@canonical_source(
    "Source", filename="source.md", merge_policy="local", heading="identity"
)
class SOURCE:
    class SECTION_001:
        """Source section."""

        related @= (TARGET.SPEC_001,)
