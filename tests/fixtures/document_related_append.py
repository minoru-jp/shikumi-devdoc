"""Canonical document showing that related is an ordinary appended field."""

from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import canonical_source
from tests.fixtures.document_related_targets import API_TARGET, SPEC_TARGET


@canonical_source(
    "Relations", filename="relations.md", merge_policy="local", heading="identity"
)
class RELATIONS:
    """Ordinary document fields follow the ordinary append policy."""

    related @= (SPEC_TARGET, API_TARGET)
