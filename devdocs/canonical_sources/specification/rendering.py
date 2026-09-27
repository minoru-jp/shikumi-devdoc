"""Rendering specification part."""

from shikumi_devdoc.fields.specification import MUST, SHOULD, condition, level, related
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.specification.specification import SPECIFICATION_PART as SPECIFICATION_SPEC
from devdocs.canonical_sources.specification.core import SPECIFICATION_PART as CORE_SPEC


@summary('Markdown 実現、realization context、canonical document 境界に関する規則。')
@canonical_source("Rendering", filename="rendering.md", order=70, placeholders=True, heading="identity")
class SPECIFICATION_PART:
    """Markdown 実現、realization context、canonical document 境界に関する規則。"""

    class RENDER_001:
        """標準 Markdown realizer は実現前に `check()` で実現可能性を診断できなければならない。"""

        title @= "Realization check"
        level @= MUST

    class RENDER_002:
        """未知の {{TERM_012}} は空文字へ黙って置換せず診断されなければならない。"""

        merge @= TERMS.TERM_012

        title @= "Unknown context reference"
        level @= MUST
        condition @= "canonical document または Glossary を実現する場合。"

    class RENDER_003:
        """複数ファイルを生成する標準 realizer は、出力 filename と本文を持つ `MarkdownDocument` の集合として成果物を返さなければならない。{{TERM_002}} の filename は各 root の `@canonical_source(..., filename=...)` 宣言から決定する。"""

        merge @= TERMS.TERM_002

        title @= "Partition output"
        level @= MUST
        related @= (SPECIFICATION_SPEC.SPEC_003,)

    class RENDER_004:
        """{{TERM_002}} を後続の翻訳工程へ渡す場合は、{{TERM_014}} の {{TERM_017}} 方針を `TranslationSourceRealizer` によって機械可読メタデータとして埋め込んでよい。"""

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_017

        title @= "Translation metadata"
        level @= SHOULD

    class RENDER_005:
        """生成物先頭の運用コメントは利用側から明示的に与えられ、realizer がプロジェクト固有文言を自動探索してはならない。"""

        title @= "Header comments are caller supplied"
        level @= MUST
    class RENDER_006:
        """標準 index realizer は document system で package を検証した SemanticView を入力とし、その package tree に含まれる `@canonical_source(...)` {{TERM_001}} root を収集して一つの Markdown index を生成しなければならない。module focus から collection index を生成してはならない。"""

        merge @= TERMS.TERM_001

        title @= "Package-level collection index"
        level @= MUST
        related @= (SPECIFICATION_SPEC.SPEC_009, SPECIFICATION_SPEC.SPEC_011)
    class RENDER_007:
        """標準 index realizer は索引対象となる各 {{TERM_002}} に `@summary(...)` metadata を要求し、索引には document title へのリンクと summary を提示しなければならない。{{TERM_001}} path のような作者側の実装詳細を索引本文へ露出してはならない。"""

        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_001

        title @= "Index summary metadata"
        level @= MUST
    class RENDER_008:
        """標準 document Markdown realizer は nested document node を ATX heading として実現し、semantic reference に使う logical fragment を実際に出力する heading text から決定論的に導出しなければならない。`heading="title"` では解決済み `title @= ...` を見出しに使用し、title がない node は class identity へ fallback する。`heading="identity"` では title の有無にかかわらず class identity を見出しに使用し、title がある場合は human-readable metadata として本文側へ実現する。標準 fragment 変換は GitHub 互換の heading slug 規則を logical reference convention として採用し、heading text を strip・小文字化し、Unicode の英数字・`-`・`_`・空白だけを残した後、連続する空白を `-` へ置換する。これは Markdown 標準による fragment 保証ではなく、downstream renderer が異なる規則を使う場合の調整は publication 側の責務とする。明示 HTML anchor を追加してはならない。"""

        title @= "Heading-derived logical fragments"
        level @= MUST

    class RENDER_009:
        """reference presentation の値が canonical document node を指す場合、標準 document Markdown realizer は参照元と参照先の canonical document logical path から相対 document path を決定し、参照先で実際に出力される heading text から導出した logical fragment と組み合わせて logical Markdown link を生成しなければならない。同一 document 内では fragment-only link を使用してよい。参照先 document が同じ実行で生成されたか、filesystem 上に存在するか、realization の出力 directory、または最終公開先で同じ相対配置になるかを探索・推論してはならない。"""

        title @= "Logical reference links"
        level @= MUST
        related @= (CORE_SPEC.CORE_012,)

    class RENDER_010:
        """publication process が canonical document logical path の相対関係、filename、または downstream Markdown renderer の heading-fragment 規則を変更する場合、必要な link rewrite は publication 側の責務としなければならない。その差異を理由に canonical source の semantic relation を Markdown path や fragment へ置き換えてはならない。"""

        title @= "Publication layout owns link rewrites"
        level @= MUST
    class RENDER_011:
        """canonical document root 自体は filename によって semantic reference target にできる。nested canonical document node を `reference_field` の target にする場合、その target を含む root は `heading="identity"` を使用しなければならない。`heading="title"` の nested heading は title、Vocabulary term、context の変更によって fragment が変化し得るため、stable semantic reference target として扱ってはならない。"""

        title @= "Stable nested reference targets require identity headings"
        level @= MUST

