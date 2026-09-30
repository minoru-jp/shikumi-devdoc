# DOC-SNIPPET readme-dogfood-readme START
from shikumi_devdoc.norms.common import IGNORE, canonical_source
from shikumi_devdoc.norms.document import test_target_field, title


example_source = test_target_field("example source")


@canonical_source(
    "{{project.name}}",
    filename="README.md",
    merge_policy="all",
    unreferenced_fields=IGNORE,
    heading="title",
)
class SECTION_001:
    r"""
    `{{project.name}}` は、仕様や設計文書を
    実装と一緒に育てるためのライブラリです。

    ```python
    {{example_source}}
    ```
    """

    example_source @= r"""
    from shikumi_devdoc.norms.common import canonical_source


    @canonical_source("Example", filename="example.md", merge_policy="local", heading="identity")
    class EXAMPLE:
        class Introduction:
            "Hello from shikumi-devdoc."
    """

    class SECTION_002:
        """このプロジェクト自身の文書も、この仕組みで管理しています。"""

        title @= "このプロジェクト自身がサンプルです"
# DOC-SNIPPET readme-dogfood-readme END
