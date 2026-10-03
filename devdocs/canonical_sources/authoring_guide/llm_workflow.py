"""LLM-assisted authoring workflow."""

from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import IGNORE, canonical_source, merge, summary
from shikumi_devdoc.norms.document import title


@summary(
    "LLM が目的文書を選び、必要な canonical source だけを変更して検証・再生成するための作業順序。"
)
@canonical_source(
    "LLM authoring workflow",
    filename="llm-workflow.md",
    order=120,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """LLM は作成する文書の目的を先に特定し、その authoring pattern を主な作業指示として使う。"""

    class SECTION_001:
        r"""
        repository を読んだからといって README、Specification、API Reference、CHANGELOG、Glossary を一式作らない。利用者の目的、既存の公開 surface、保守上必要な契約を確認し、必要な文書だけを選ぶ。

        新規作成では [Authoring Guide overview](overview.md) から目的別ページを選ぶ。既存 repository の修正では、まず現在の文書体系と canonical source の境界を読み、既存責務を尊重する。
        """

        title @= "最初に必要な文書だけを決める"

    class SECTION_002:
        r"""
        Specification を作るなら Specification page、API Reference を作るなら API Reference page の推奨構造から開始する。複数の機能別ページを先にすべて読んで独自の組み合わせを設計しない。

        細部の契約が不明なときだけ Specification / API Reference を参照し、特殊な横断判断が必要なときだけ Advanced authoring を読む。
        """

        title @= "目的別ページを主な指示として使う"

    class SECTION_003:
        r"""
        {{TERM_002}} や published Markdown の表現だけを局所修正せず、対応する {{TERM_001}}、Vocabulary、realization context へ変更を戻す。validation と realization を通して成果物を再生成し、生成差分を確認する。
        """

        title @= "生成物ではなく canonical source を編集する"

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_001

    class SECTION_004:
        r"""
        LLM は規則を見つけるとすべて field 化・Vocabulary 化・分割しやすい。各構造化には validation、再利用、安定 identity、presentation、テスト可能性など具体的な利点を要求し、単なる文章は prose のまま残す。

        同じ理由で、文書数を増やすこと自体を改善とみなさない。読者の目的と変更責務が独立するときだけ collection 化する。
        """

        title @= "過剰な構造化を避ける"
