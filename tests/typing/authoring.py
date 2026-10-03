"""Consumer-side static typing contract for canonical-document authoring DSL."""

from __future__ import annotations

from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import field

added = field("Added", str)
identity_field = field("Identity", str)


class TargetA:
    pass


class TargetB:
    pass


@canonical_source(
    "Typing contract",
    filename="typing-contract.md",
    merge_policy="local",
    heading="identity",
)
class TYPING_CONTRACT:
    """{{identity}}"""

    # Repeated field writes must preserve an augmented-assignment-capable binding.
    added @= "first"
    added @= "second"

    # A field binding can be captured by merge and then extended without losing
    # the identity that merge observed at runtime.
    identity_field @= "first"
    merge @= ("identity", identity_field)
    identity_field @= "second"

    # Repeated merge declarations likewise remain valid after the first @=.
    merge @= TargetA
    merge @= TargetB
