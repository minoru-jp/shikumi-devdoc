from shikumi_devdoc.norms.document import (
    field,
    list_field,
    table_field,
    test_target_field,
)

level = field("level", str)
requirement_status = field("status", str)
tag = field("tag", str, many=True)
related = field("related", type, many=True)
steps = list_field("steps", str)
example = test_target_field("example")
compatibility = table_field("compatibility", columns=("runtime", "status"))
