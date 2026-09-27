"""Canonical document exercising same-document semantic references."""

from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source("Same-document references", filename="same-references.md", placeholders=False, heading="identity")
class SAME_REFERENCES:
    """See {{related}} for the stable target."""

    class SECTION_001:
        """Target section."""
        title @= "Natural target title"

    related @= (SECTION_001,)
