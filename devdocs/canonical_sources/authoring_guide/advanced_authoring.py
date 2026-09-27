"""Cross-cutting advanced authoring guidance."""

from devdocs.canonical_sources.specification.document import SPECIFICATION_PART as DOCUMENT_SPEC
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source, merge, summary
from shikumi_devdoc.norms.document import test_target_field, title


indented_docstring_example = test_target_field("indented docstring example")
section_identity_example = test_target_field("opaque section identity example")
documented_snippet = test_target_field("documented snippet")


@summary("目的別パターンで足りない場合に使う prose/field、identity、reference、context、code example の横断判断。")
@canonical_source(
    "Advanced authoring decisions",
    filename="advanced-authoring.md",
    order=110,
    placeholders=False,
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """通常は目的別 authoring pattern を優先し、ここは横断的な設計判断が必要な場合だけ参照する。"""

    class SECTION_001:
        r"""
        背景、理由、説明の流れなど文章として読むことで意味が成立する内容は prose に置く。比較、列挙、再利用、validation、特定 presentation に具体的な価値がある意味情報だけを {{TERM_007}} へ分離する。

        構造化できるものをすべて field にしない。`field`、`list_field`、`table_field`、`prose_field`、`reference_field` は必要な情報構造を分離するために使う。`test_target_field` は presentation のためではなく、通常のテストから直接参照したい literal text を正本上で独立させるために使う。
        """
        title @= "Prose と field を分ける"

        merge @= TERMS.TERM_007

    class SECTION_002:
        r"""
        nested node の human-readable title は `title @= "..."` に統一する。`@title(...)` decorator は使用しない。`title` は同じ node の `merge` と realization context を解決できるため、Vocabulary の正式名称を見出しへ安全に反映できる。

        narrative document では `@canonical_source(..., heading="title")` を選ぶと、解決済み title が Markdown heading になる。node に意味名を持たせる必要がない場合は `SECTION_NNN` のような opaque identity を推奨する。`NNN` は表示順、見出しレベル、公開節番号を表さない。並べ替え、title 変更、階層移動でも既存 identity は維持する。

        ```python
        {{section_identity_example}}
        ```

        stable nested reference target が必要な document では `heading="identity"` を選ぶ。この場合 identity が見出しとなり、title は human-readable metadata として出力される。これは authoring convention であり identity の命名形式自体は validator が強制しない。Specification の `SPEC_NNN` など、目的文書に適した identity scheme を使ってよい。
        """
        title @= "Node identity と表示 title を分離する"

        section_identity_example @= r'''
        @canonical_source("Guide", filename="guide.md", heading="title", placeholders=False)
        class GUIDE:
            class SECTION_017:
                """Introductory text."""
                title @= "Getting started"
        '''
        related @= (DOCUMENT_SPEC.DOC_001, DOCUMENT_SPEC.DOC_003)

    class SECTION_003:
        r"""
        canonical root と document node の docstring は意味内容へ取り込まれる前に `inspect.cleandoc()` 相当で正規化される。Python scope に合わせて本文をインデントしてよく、共通 indent は除去され、本文内部の相対 indent は保持される。

        raw / non-raw、triple single / double quote は authoring 上必要な形式を選べる。

        ```python
        {{indented_docstring_example}}
        ```
        """
        title @= "Docstring は自然にインデントする"

        indented_docstring_example @= r'''
        class SECTION_001:
            """
            Introductory text.

                Relative indentation is preserved.
            """
        '''

    class SECTION_004:
        r"""
        field binding の `name @= value` は同じ node の template から `\{{name}}` として参照できる。Vocabulary term などの class target は `merge @= target`、明示 alias が必要なら `merge @= ("name", target)` を使う。

        merge を一般的な macro system として長い文章の断片化に使わない。docstring、`prose_field`、`title @= ...` は template-bearing content、通常の scalar/list/table/test target field value は literal content である。
        """
        title @= "Local reference は node 内に閉じる"

    class SECTION_005:
        r"""
        同じ canonical source を将来再実現したとき値が変わってよいなら {{TERM_005}} の候補になる。現在の project version などは context に向く。過去の release version、採用済み設計判断、規範条件など後から変えてはいけない事実は canonical source に置く。
        """
        title @= "Realization context は変化してよい外部値だけに使う"

        merge @= TERMS.TERM_005

    class SECTION_006:
        r"""
        実装 drift を検出したい sample code、設定、command、expected output などは `test_target_field` へ分離し、値そのものを pytest など通常のテストから検証する。fence や language 指定は surrounding docstring に書く。文書生成時に `eval` / `exec` する特殊なテスト DSL を作らない。

        ```python
        {{documented_snippet}}
        ```
        """
        title @= "Code example は通常のテストで保護する"

        documented_snippet @= r'''
        from shikumi_devdoc.norms.common import canonical_source
        from shikumi_devdoc.norms.document import test_target_field, title

        example = test_target_field("example")

        @canonical_source("Guide", filename="guide.md", placeholders=False, heading="title")
        class GUIDE:
            class SECTION_001:
                """
                ```python
                {{example}}
                ```
                """
                title @= "Example"
                example @= """
                print("hello")
                """
        '''
    class SECTION_007:
        r"""
        Python object 間の関係を公開 Markdown でも辿れる形にしたい場合は `reference_field()` を使う。標準 `related` はその convenience field である。canonical source には Markdown filename や fragment を書かず object relation を保持する。

        nested node を stable semantic reference target にする場合、参照先 document は `heading="identity"` を使用する。`heading="title"` の見出しは title、Vocabulary、context の変更で fragment が変化し得るため `related` などの nested target にはできない。document root 自体は filename で参照できるためこの制限を受けない。

        Markdown realizer は canonical source の出自から導出した source/target の canonical document logical path を相対化し、参照先 identity heading から導出した logical fragment と組み合わせて logical link を決定論的に生成する。明示 HTML anchor は追加しない。実際の publication layout や downstream Markdown renderer の fragment 規則は探索・推論・検証しない。通常は canonical document の logical topology と GitHub 互換の heading slug 規則を保てばそのまま有効なリンクになる。公開時に配置や fragment 規則が変わる場合は publication processing で realized link を修正する。
        """
        title @= "Semantic reference と publication link を分離する"

