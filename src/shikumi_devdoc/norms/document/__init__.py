"""Generic canonical-document authoring API."""

from .._document import (
    test_target_field,
    document as system,
    field,
    list_field,
    prose_field,
    reference_field,
    table_field,
    title,
)

__all__ = [
    "test_target_field",
    "field",
    "list_field",
    "prose_field",
    "reference_field",
    "system",
    "table_field",
    "title",
]
