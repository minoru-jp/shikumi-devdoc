"""Canonical document referring to a nested target rendered independently."""

from tests.fixtures.document_reference_nested_target import SPEC_050
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Reference source", filename="source.md", merge_policy="local", heading="identity")
class SOURCE:
    """The target document does not need to be part of this realization."""

    related @= (SPEC_050,)
