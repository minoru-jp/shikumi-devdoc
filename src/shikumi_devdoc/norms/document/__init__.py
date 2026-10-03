"""Generic canonical-document authoring API."""

from .._document import (
    document as system,
)
from .._document import (
    field,
    list_field,
    prose_field,
    reference_field,
    table_field,
    test_target_field,
    title,
)

__all__ = [
    "field",
    "list_field",
    "prose_field",
    "reference_field",
    "system",
    "table_field",
    "test_target_field",
    "title",
]
