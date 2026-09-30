from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import test_target_field

example = test_target_field("example")


@canonical_source(
    "Snapshot",
    filename="snapshot-field.md",
    merge_policy="forbidden",
    heading="identity",
)
class DOCUMENT:
    """Example:\n\n    ```python\n    {{example}}\n    ```\n    """

    example @= "print('{{PROJECT.version}}')"
