"""Standard convenience fields for API-reference-like documents."""

from shikumi_devdoc.norms.document import field

from .common import detail, kind, related


name = field("name", str)
input = field("input", str, many=True)
output = field("output", str, many=True)

NAMESPACE = "Namespace"
TYPE = "Type"
VALUE = "Value"
OPERATION = "Operation"
OTHER = "Other"

API_NAMESPACE = NAMESPACE
API_TYPE = TYPE
API_VALUE = VALUE
API_OPERATION = OPERATION
API_OTHER = OTHER


__all__ = [
    "API_NAMESPACE",
    "API_OPERATION",
    "API_OTHER",
    "API_TYPE",
    "API_VALUE",
    "NAMESPACE",
    "OPERATION",
    "OTHER",
    "TYPE",
    "VALUE",
    "detail",
    "input",
    "kind",
    "name",
    "output",
    "related",
]
