"""Canonical document containing a nested reference target."""

from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source("Runtime targets", filename="runtime-targets.md", merge_policy="local", heading="identity")
class RUNTIME_TARGETS:
    class SECTION_502:
        title @= "Runtime target resolution"
        class SPEC_050:
            """Stable normative target."""


SPEC_050 = RUNTIME_TARGETS.SECTION_502.SPEC_050
