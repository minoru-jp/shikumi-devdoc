"""Getting-started authoring pattern."""

from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import test_target_field, title


quickstart_example = test_target_field("quick-start command")


@summary("初回利用者を一つの成功体験まで案内する task-oriented guide の作り方。")
@canonical_source(
    "Writing a Getting Started guide",
    filename="getting-started.md",
    order=20,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """Getting Started は reference ではなく、最短の成功経路を順番に案内する。"""

    class SECTION_001:
        r"""
        README の最小例だけでは初回利用に必要な手順を説明しきれない場合に作る。読者が installation から一つの成功結果まで順番に進むための文書であり、全機能を網羅する reference ではない。
        """
        title @= "Getting Started を作る場合"

    class SECTION_002:
        r"""
        最も一般的で依存関係の少ない利用経路を一つ選び、前提条件、installation、最小設定、実行、期待結果の順に記述する。途中で複数の選択肢を大量に提示せず、代替手段は成功後の「次に読む文書」へ送る。
        """
        title @= "一つの happy path を選ぶ"

    class SECTION_003:
        r"""
        command、Python snippet、設定例などを通常のテストから直接検証したい場合だけ `test_target_field` に分離する。表示用の Markdown fence は docstring 側に書き、通常のテストスイートで field 値そのものを検証する。

        ```bash
        {{quickstart_example}}
        ```
        """
        title @= "実行可能な例を優先する"

        quickstart_example @= "example --help"

    class SECTION_004:
        r"""
        Getting Started では、その手順に必要な設定や option だけを説明する。完全な設定一覧は Configuration Guide、完全な option 一覧は CLI documentation、契約上の例外条件は Specification へリンクする。
        """
        title @= "Reference を複製しない"
