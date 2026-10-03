from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import (
    field,
    list_field,
    table_field,
    test_target_field,
)

scalar = field("scalar", str)
items = list_field("items", str)
code = test_target_field("code")
table = table_field("table", columns=("expression", "meaning"))


@canonical_source(
    "Literal fields",
    filename="literal-fields.md",
    merge_policy="local",
    heading="identity",
)
class LITERAL_FIELDS:
    """Literal test target:

    ```jinja
    {{code}}
    ```
    """

    scalar @= "{{PROJECT.version}}"
    items @= "{{scalar}}"
    code @= "Hello {{ user.name }}"
    table @= ("{{PROJECT.version}}", "literal")
