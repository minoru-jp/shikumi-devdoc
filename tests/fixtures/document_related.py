"""Canonical document with semantic relations to Specification and API entities."""

from tests.fixtures.document_related_targets import API_TARGET, SPEC_TARGET
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source("Guide", filename="document_related.md", merge_policy="all", unreferenced_fields=IGNORE, heading="title")
class TITLE_1:
    """Purpose-oriented explanation whose source records structured relations."""

    related @= (SPEC_TARGET, API_TARGET)

    class TITLE_2:
        """The rendered prose remains independent of relation presentation."""
        title @= "Usage"

        related @= (SPEC_TARGET,)
