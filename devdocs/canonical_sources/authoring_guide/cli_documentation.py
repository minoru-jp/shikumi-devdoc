"""CLI-documentation authoring pattern."""

from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import test_target_field, title


cli_example = test_target_field("CLI example")


@summary("CLI の基本操作、argument、mode、出力を task-oriented に説明する方法。")
@canonical_source(
    "Writing CLI documentation",
    filename="cli-documentation.md",
    order=40,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """CLI documentation は command-line 利用者が目的の操作へ到達するための guide/reference とする。"""

    class SECTION_001:
        r"""
        command-line interface が主要な公開 surface で、README の最小例だけでは argument、mode、入出力、安全条件を十分に説明できない場合に作る。
        """
        title @= "CLI documentation を作る場合"

    class SECTION_002:
        r"""
        parser 内部の実装順ではなく、利用者の操作単位で章を分ける。例えば basic invocation、input/target selection、mode、preview/output、exit/error behavior のように、調べる目的が異なるものを分離する。

        一枚が長くなる場合は同じ意味領域で collection 化する。単に option 数が多いという理由だけで細かくファイル分割しない。
        """
        title @= "操作のまとまりで構成する"

    class SECTION_003:
        r"""
        文書に掲載する command は、通常のテストから文字列そのものを検証したい場合に `test_target_field` へ分離する。表示用の `bash` fence は docstring 側に書く。

        ```bash
        {{cli_example}}
        ```

        option 名や invocation shape が実装と drift しやすい場合は、parser test または CLI integration test と対応させる。
        """
        title @= "Command 例をテスト可能にする"

        cli_example @= "example --input src --output build"

    class SECTION_004:
        r"""
        CLI document は「どう使うか」を中心にする。default の決定規則、複数 option の衝突、禁止組み合わせ、exit contract など互換性上の規範は Specification がある場合そちらへ置き、CLI document から対応ページへリンクする。
        """
        title @= "厳密な契約は Specification へ置く"
