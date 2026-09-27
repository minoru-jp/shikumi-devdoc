"""Authoring Guide overview."""

from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import IGNORE, canonical_source, merge, summary
from shikumi_devdoc.norms.document import title


@summary("必要な文書だけを選び、目的文書ごとの推奨パターンから authoring を始めるための総則。")
@canonical_source(
    "Authoring Guide overview",
    filename="overview.md",
    order=0,
    placeholders=False,
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    r"""
    このガイドは、`shikumi-devdoc` で {{TERM_001}} を設計・保守するときの実践的な判断指針をまとめる。[Specification](../specification/INDEX.md) は保証される振る舞いを、[API Reference](../api/INDEX.md) は公開インターフェースを記述する。Authoring Guide は、それらの仕組みを使って「目的の文書をどう書くか」を案内する。

    主な読者として、人間だけでなく LLM がリポジトリの文書体系を設計・更新する場合を想定する。このため、フレームワーク機能の分類ではなく、作成したい文書から読み始められる構成を優先する。
    """

    merge @= TERMS.TERM_001

    class SECTION_001:
        r"""
        `shikumi-devdoc` は、README、Specification、API Reference、CHANGELOG、Glossary などをすべて配置することをリポジトリへ要求しない。必要な文書だけを作ればよい。小さなライブラリで README だけが必要なら README だけを canonical source にしてよく、公開契約を厳密に管理する project なら Specification や API Reference を追加してよい。

        このガイドに挙げる文書は必須の document type ではなく、generic canonical-document model の推奨 authoring pattern である。project に当てはまらない文書を形式的に作らない。逆に、ここに名前のない文書も同じ generic model で自由に作成できる。
        """
        title @= "特定の文書セットを要求しない"

    class SECTION_002:
        r"""
        作業を始めるときは、最初に目的文書を決め、そのページを主な作業手順として使う。

        - [README を書く](readme.md): repository の入口、概要、最小利用例、詳細文書への導線を作る。
        - [Getting Started を書く](getting-started.md): 初回利用者を一つの成功体験まで案内する。
        - [Configuration Guide を書く](configuration-guide.md): 設定の書き方、発見、組み合わせ、例を説明する。
        - [CLI documentation を書く](cli-documentation.md): command-line 利用者が操作を調べられる文書を作る。
        - [Specification を書く](specification.md): 実装や互換性が従う規範的な契約を構造化する。
        - [API Reference を書く](api-reference.md): 公開 API の名前、種別、入力、出力、詳細、lifecycle を記録する。
        - [CHANGELOG を書く](changelog.md): release 単位の変更履歴を記録する。
        - [Glossary / Vocabulary を書く](glossary.md): 複数文書で共有する概念名称と定義を一元管理する。
        - [Project Status を書く](project-status.md): 現在状態、方向性、利用者への告知を記録する。
        - [複数文書の collection を作る](collections.md): 大きな文書を意味領域ごとの独立 document に分割する。

        特殊な設計判断が必要になった場合だけ、[Advanced authoring](advanced-authoring.md) を参照する。LLM が作業する場合は [LLM workflow](llm-workflow.md) も作業境界として使う。
        """
        title @= "まず作りたい文書を選ぶ"

    class SECTION_003:
        r"""
        Markdown の見た目からではなく、{{TERM_001}} 上で何を意味として保持するかから設計する。構造化には validation、presentation、再利用、名称の一元管理など具体的な目的を持たせる。明確な利点がない情報は通常の prose でよい。

        {{TERM_002}} はレビュー可能な成果物だが、内容変更の起点にはしない。変更は {{TERM_001}} または必要な {{TERM_005}} に戻し、validation と realization を通して再生成する。

        文書を増やすこと自体を目標にしない。既存の文書で目的を満たせるなら新しい文書を追加せず、責務が明確に分かれる場合だけ分割する。
        """
        title @= "基本原則"

        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_005

    class SECTION_004:
        r"""
        各 authoring pattern は、そのページを読めば少なくとも最初の canonical source を作成できるように、作成すべき場合、推奨構造、使う field、例、避けるべき設計をまとめる。

        Specification や API Reference の完全な契約を Authoring Guide に複製しない。細部の挙動が必要な場合は Specification / API Reference を参照する。ただし、作者が基本的な文書を作るために複数の機能別ガイドを巡回しなければならない構成にはしない。
        """
        title @= "目的別ページだけで着手できるようにする"
