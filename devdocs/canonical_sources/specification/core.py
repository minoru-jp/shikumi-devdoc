"""Core specification part."""

from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.fields.specification import INFORMATIVE, MUST, level
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title


@summary("canonical source と文書体系全体に共通する中核規則。")
@canonical_source(
    "Core", filename="core.md", order=0, merge_policy="local", heading="identity"
)
class SPECIFICATION_PART:
    """文書体系全体に共通する中核規則。"""

    class CORE_001:
        """{{TERM_002}} を構成する権威ある各文書ソース単位は `@canonical_source` によって明示されなければならない。bare `@canonical_source` は Vocabulary のような非文書 {{TERM_001}} にも使用できる。"""

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_001
        title @= "Canonical source"
        level @= MUST

    class CORE_002:
        """標準 realizer へ渡す意味像は、対応する規定体による検証に成功していなければならない。"""

        title @= "Validate before realization"
        level @= MUST

    class CORE_003:
        """README は入口、Project Status は現在と現在から見た未来、Specification は現行規則、API Reference は公開インターフェース、CHANGELOG は過去の変更を担当する。これらは `shikumi-devdoc` の専用文書型ではなく、利用側が共通 document model 上に構成するドメイン文書であってよい。"""

        title @= "Public documentation roles"
        level @= INFORMATIVE

    class CORE_004:
        """{{TERM_002}} は、{{TERM_001}} を対応する規定体で検証し、必要な {{TERM_005}} を注入し、realizer によって文書として組み立てた結果である。`shikumi-devdoc` が一貫して扱う文書成果物の責務境界は {{TERM_002}} までとする。"""

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_005
        title @= "Canonical document"
        level @= INFORMATIVE

    class CORE_005:
        """{{TERM_005}} は、現在版など {{TERM_001}} に固定せず実現時点で外部から与える値の入力である。Context は歴史的事実の保存先や、{{TERM_001}} の代替となる正本を意味しない。"""

        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_001
        title @= "Realization context"
        level @= INFORMATIVE

    class CORE_006:
        """{{TERM_003}} は {{TERM_002}} から翻訳、ローカライズ、表現調整、媒体変換、配布などの公開工程で作られる派生物である。これらの {{TERM_004}} は利用側の事情に依存し、`shikumi-devdoc` は特定の公開方法を規定しない。"""

        merge @= TERMS.TERM_003
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_004
        title @= "Published document boundary"
        level @= INFORMATIVE

    class CORE_007:
        """`@canonical_source` が記録する {{TERM_001}} の出自は、その Python module の構造から安定して決定され、プロセスの current working directory に依存してはならない。"""

        merge @= TERMS.TERM_001
        title @= "Canonical source provenance"
        level @= MUST

    class CORE_008:
        """{{TERM_002}} の root title、filename、nested heading policy、任意 order、merge policy、未参照 field policy は文書内容の意味論から独立した共通 metadata として `@canonical_source(...)` に宣言されなければならない。nested heading policy は `heading="title"` または `heading="identity"` のどちらかを作者が明示し、realizer が文書種別から推論してはならない。"""

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_012
        title @= "Canonical document metadata"
        level @= MUST

    class CORE_009:
        """{{TERM_002}} は単一の {{TERM_006}} model を使用しなければならない。root と nested class は同じ node model を共有し、docstring template、作者定義 {{TERM_007}}、nested class hierarchy の組合せによって文書を構成しなければならない。"""

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_007
        title @= "Unified canonical document model"
        level @= MUST

    class CORE_010:
        r"""`@canonical_source(..., merge_policy=...)` は {{TERM_010}} へ明示的に値を取り込む経路として、`merge @= ...` による local merge と {{TERM_012}} の許可範囲を `"all"`、`"local"`、`"external"`、`"forbidden"` の4段階で制御しなければならない。`"all"` は双方、`"local"` は local merge のみ、`"external"` は {{TERM_012}} のみを許可し、`"forbidden"` は双方を禁止する。未指定時は `"all"` とする。同じ {{TERM_006}} に直接 `name @= value` として定義された field binding はこの制約の対象外とし、すべての policy で {{TERM_010}} から参照できなければならない。"""

        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_012
        title @= "Merge policy"
        level @= MUST

    class CORE_010A:
        r"""`merge_policy="external"` または `merge_policy="forbidden"` の canonical document は、使用の有無にかかわらず `merge @= ...` 宣言を持ってはならない。この禁止は同じ {{TERM_006}} に直接定義された field binding の {{TERM_013}} 参照には適用してはならない。`merge_policy` は `name @= value` の Python 評価前の由来を追跡する provenance 制約ではなく、明示的な merge/context 経路だけを制約しなければならない。通常の field value は {{TERM_011}} として保持でき、その内部の placeholder-like text は template 解釈してはならない。"""

        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_011
        merge @= TERMS.TERM_013
        title @= "Local merge prohibition"
        level @= MUST

    class CORE_010B:
        r"""非推奨の `placeholders=True` は `merge_policy="all"`、`placeholders=False` は `merge_policy="local"` と等価に解釈されなければならない。`placeholders` と `merge_policy` を同時指定してはならない。`placeholders` の使用は API 直接利用時にも deprecation warning を送出し、CLI 利用時にはその warning が利用者へ表示されなければならない。`placeholders` は 1.0.0 で削除予定とする。"""

        title @= "Legacy placeholders compatibility"
        level @= MUST

    class CORE_011:
        """`unreferenced_fields=APPEND` は template から参照されなかった {{TERM_007}} を各 {{TERM_006}} の末尾へ実現し、`unreferenced_fields=IGNORE` はそれらを {{TERM_001}} 上の情報として保持したまま {{TERM_002}} へ出力しない policy でなければならない。"""

        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002
        title @= "Unreferenced field policy"
        level @= MUST

    class CORE_012:
        """canonical document の logical path は、`CanonicalSource` が記録する Python module provenance の親 path と、root に宣言された canonical filename の組合せから決定論的に導出されなければならない。この logical path は canonical document体系上の出自と相対配置を表し、realization の出力 directory や published document の配置を表してはならない。"""

        title @= "Canonical document logical path"
        level @= MUST
