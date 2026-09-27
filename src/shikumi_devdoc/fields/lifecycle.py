"""Standard convenience fields for documenting subject lifecycle changes."""

from shikumi_devdoc.norms.document import field, prose_field


introduced = field("introduced", str)
deprecated = field("deprecated", str)
removed = field("removed", str)
replacement = field("replacement", (str, type), many=True)
migration = prose_field("migration")


__all__ = [
    "deprecated",
    "introduced",
    "migration",
    "removed",
    "replacement",
]
