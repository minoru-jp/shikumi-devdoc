"""Reusable standard fields shared by multiple document profiles."""

from shikumi_devdoc.norms.document import field, reference_field


kind = field("kind", str)
condition = field("condition", str, many=True)
detail = field("detail", str, many=True)
related = reference_field("related", (type, tuple), many=True)


__all__ = [
    "condition",
    "detail",
    "kind",
    "related",
]
