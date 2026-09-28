"""Specification authoring pattern."""

from devdocs.canonical_sources.specification.specification import SPECIFICATION_PART as STRUCTURED_SPEC
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import test_target_field, title


specification_example = test_target_field("specification example")


@summary("規範的な契約を SPEC_NNN node と specification field set で構造化する方法。")
@canonical_source(
    "Writing a Specification",
    filename="specification.md",
    order=50,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """Specification は実装や互換性が従う契約を、narrative guide から分離して記述する。"""

    class SECTION_001:
        r"""
        実装間で一致させる必要がある規則、互換性を判断する契約、曖昧さを残したくない edge case がある場合に作る。小さな project で README や API contract だけで十分なら、Specification を追加する必要はない。
        """
        title @= "Specification を作る場合"

    class SECTION_002:
        r"""
        Specification root では原則として `@canonical_source(..., heading="identity")` を指定する。規範文を大きな docstring に連続して埋め込まず、一つの規則として参照・変更する価値がある単位を独立 node にする。stable identity が必要な場合は `SPEC_NNN` のような opaque identity を使い、表示順や節番号として扱わない。human-readable title は `title @= ...` に置くため、title や Vocabulary の変更で stable fragment は変化しない。

        説明だけをまとめる container section は `SECTION_NNN` などの narrative identity でよい。
        """
        title @= "規則を独立 node にする"

    class SECTION_003:
        r"""
        `shikumi_devdoc.fields.specification` は `level`、`condition`、`detail`、`related` と、`MUST` / `MUST_NOT` / `SHOULD` / `SHOULD_NOT` / `MAY` / `INFORMATIVE` を提供する。必要な field だけを使う。human-readable title は field set ではなく `shikumi_devdoc.norms.document.title` で `title @= ...` と記述する。

        ```python
        {{specification_example}}
        ```
        """
        title @= "標準 field set を使う"

        specification_example @= r'''
        from shikumi_devdoc.fields.specification import MUST, condition, level
        from shikumi_devdoc.norms.document import title

        class SPEC_001:
            """The implementation returns an error when the input is invalid."""

            title @= "Invalid input"
            level @= MUST
            condition @= "The input fails validation."
        '''
        related @= (STRUCTURED_SPEC.SPEC_007,)

    class SECTION_004:
        r"""
        `related` は「see also」を相互に張るためではなく、その規則を理解・成立させるために依存する意味対象を示す一方向 relation として使うと保守しやすい。依存する側から基礎側へ参照し、逆方向の backlink は source に重複して書かない。

        Python import が循環する場合は、遅延参照で回避する前に文書構造を見直す。共通規則を基礎 document へ抽出できないか、単なる関連であって依存ではないかを確認し、可能な限り循環した規範構造を作らない。

        `related` の nested target は `heading="identity"` の canonical document に属していなければならない。`heading="title"` の nested node を target にすると title 変更や Vocabulary 変更が別文書の再生成を要求するため、validator が拒否する。document root 自体は filename で参照できるので例外である。

        `related` には Markdown filename や `#fragment` を書かず Python object relation を保つ。Markdown realizer は canonical source の出自から導出した source/target の canonical document logical path を相対化し、identity heading から導出した logical fragment と組み合わせて link を生成する。この logical path は realization の出力先ではなく canonical document 体系上の相対配置を表す。通常はその logical topology と GitHub 互換の heading slug 規則を保って公開すればリンクはそのまま有効になる。publication 側で filename、directory、または fragment 規則を変更する場合は、翻訳・公開処理で realized Markdown link を修正し、canonical `related` を公開 URL に合わせて変更しない。
        """
        title @= "related は依存方向を表す"

    class SECTION_005:
        r"""
        path、configuration、output、CLI contract のように独立して変更・参照できる領域が育った場合は、一枚の巨大な Specification を保たず document collection へ分ける。各 document は単独で validation / realization できる状態を保つ。
        """
        title @= "大きくなったら意味領域で collection 化する"
