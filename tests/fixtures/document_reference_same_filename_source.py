"""Reference source using the same filename as a distinct target document."""

from tests.fixtures.document_reference_same_filename_target import SPEC_001
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Source", filename="collision.md", merge_policy="local", heading="identity")
class SOURCE:
    related @= (SPEC_001,)
