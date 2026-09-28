"""Canonical document related to a plain, already-resolved Python class."""

from tests.fixtures.related_plain_target import PLAIN_TARGET
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source("Guide", filename="document_related_plain.md", merge_policy="all", heading="identity")
class TITLE_1:
    """Relation target is resolved by Python before shikumi-devdoc sees it."""

    related @= (PLAIN_TARGET,)
