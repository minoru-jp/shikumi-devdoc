from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import field

value = field("value")


@canonical_source("External", filename="external-field.md", merge_policy="external", heading="identity")
class DOCUMENT:
    """{{value}}"""

    value @= "Local"
