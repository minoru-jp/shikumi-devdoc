"""Invalid nested semantic reference into a title-heading document."""

from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source("Narrative target", filename="target.md", merge_policy="local", heading="title")
class TARGET:
    class SECTION_001:
        """A readable but intentionally unstable nested heading target."""

        title @= "Readable target"


@canonical_source("Reference source", filename="source.md", merge_policy="local", heading="identity")
class SOURCE:
    """The document root itself is stable, but its nested title heading is not."""

    related @= (TARGET.SECTION_001,)
