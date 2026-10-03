"""Positive fixture: the documented override accepts the @= authoring style."""

from shikumi_devdoc.norms.common import merge
from shikumi_devdoc.norms.document import field, title

added = field("Added", str)


class FIRST_TARGET:
    pass


class SECOND_TARGET:
    pass


class DOCUMENT:
    title @= "Example"

    added @= "first"
    added @= "second"

    merge @= FIRST_TARGET
    merge @= SECOND_TARGET
