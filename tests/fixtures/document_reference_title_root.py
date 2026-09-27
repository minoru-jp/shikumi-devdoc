"""A title-heading document root remains a stable reference target."""

from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source(
    "Narrative target",
    filename="target-root.md",
    placeholders=False,
    heading="title",
)
class TARGET:
    class SECTION_001:
        """Readable nested content."""

        title @= "Readable target section"


@canonical_source(
    "Reference source",
    filename="source-root.md",
    placeholders=False,
    heading="identity",
)
class SOURCE:
    """A document root reference needs no heading fragment."""

    related @= (TARGET,)
