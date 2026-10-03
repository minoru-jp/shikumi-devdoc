"""Standard convenience fields for specification-like documents."""

from shikumi_devdoc.norms.document import field

from .common import condition, detail, related

level = field("level", str)

MUST = "MUST"
MUST_NOT = "MUST NOT"
SHOULD = "SHOULD"
SHOULD_NOT = "SHOULD NOT"
MAY = "MAY"
INFORMATIVE = "INFORMATIVE"


__all__ = [
    "INFORMATIVE",
    "MAY",
    "MUST",
    "MUST_NOT",
    "SHOULD",
    "SHOULD_NOT",
    "condition",
    "detail",
    "level",
    "related",
]
