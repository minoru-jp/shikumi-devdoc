from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import field, prose_field, table_field

single = field("single", str)
first = prose_field("first")
second = prose_field("second")
matrix = table_field("matrix", columns=("a", "b"))


@canonical_source(
    "Invalid fields",
    filename="invalid-fields.md",
    merge_policy="local",
    heading="identity",
)
class INVALID_FIELDS:
    """{{first}}"""

    single @= "one"
    single @= "two"
    first @= "{{second}}"
    second @= "{{first}}"
    matrix @= ("only-one",)

    merge @= ("first", first)
    merge @= ("second", second)
    merge @= ("unsupported", object())
