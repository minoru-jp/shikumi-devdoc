"""Configuration-guide authoring pattern."""

from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import test_target_field, title


configuration_example = test_target_field("configuration example")


@summary("設定ファイルの書き方、発見、合成、出力などを guide として説明する方法。")
@canonical_source(
    "Writing a Configuration Guide",
    filename="configuration-guide.md",
    order=30,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """Configuration Guide は設定を作成する利用者の作業順序と概念理解を支援する。"""

    class SECTION_001:
        r"""
        project が設定ファイル、宣言的 schema、複数 source の合成などを公開し、README の断片だけでは安全に使えない場合に作る。設定が数個の単純な値だけなら README や API Reference だけで十分な場合もある。
        """
        title @= "Configuration Guide を作る場合"

    class SECTION_002:
        r"""
        syntax の列挙だけでなく、利用者がどの設定をどこに置き、どう選択され、どう組み合わされ、どこへ影響するかを説明する。大きくなった場合は discovery、schema/reference、selection、composition、output、examples など意味領域ごとの document collection へ分ける。
        """
        title @= "利用者の判断単位で構成する"

    class SECTION_003:
        r"""
        TOML、YAML、JSON などの設定例は、parse や schema validation で値そのものを検証したい場合だけ `test_target_field` とする。通常の小さな例は docstring の fenced block に直接書いてよい。

        ```toml
        {{configuration_example}}
        ```

        `test_target_field` は Markdown fence を自動生成せず、テスト済みであることも自動保証しない。fence は docstring 側に書き、対応する parser や project の設定 loader を通常のテストから実行する。
        """
        title @= "検証対象の設定例だけ test_target_field に分離する"

        configuration_example @= r'''
        [tool.example]
        enabled = true
        '''

    class SECTION_004:
        r"""
        Guide では「どう設定すればよいか」を説明し、値の優先順位、衝突、path 解決、禁止条件など実装が従う厳密な契約がある場合は Specification に置く。Guide からは対応する specification document へリンクし、規則本文を丸ごと複製しない。
        """
        title @= "Guide と Specification を分ける"
