"""Standard convenience fields for changelog-like documents."""

from shikumi_devdoc.norms.document import field, list_field

version = field("version", str)
released_on = field("released on", str)
added = list_field("Added", str)
changed = list_field("Changed", str)
deprecated = list_field("Deprecated", str)
removed = list_field("Removed", str)
fixed = list_field("Fixed", str)
security = list_field("Security", str)


__all__ = [
    "added",
    "changed",
    "deprecated",
    "fixed",
    "released_on",
    "removed",
    "security",
    "version",
]
