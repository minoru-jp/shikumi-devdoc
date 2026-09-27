"""Referable document nodes for relation tests."""

from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Targets", filename="targets.md", placeholders=False, heading="identity")
class TARGETS:
    class SPEC_TARGET:
        """A document node referenced by another canonical document."""

    class API_TARGET:
        """Another document node referenced by another canonical document."""


SPEC_TARGET = TARGETS.SPEC_TARGET
API_TARGET = TARGETS.API_TARGET
