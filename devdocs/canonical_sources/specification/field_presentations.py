"""Field-presentation specification part."""

from shikumi_devdoc.fields.specification import MUST, MUST_NOT, SHOULD, level
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title


@summary('作者定義 field の汎用 Markdown 表現に関する規則。')
@canonical_source("Field presentations", filename="field-presentations.md", order=30, merge_policy="all", heading="identity")
class SPECIFICATION_PART:
    """作者定義 field が canonical Markdown 上で選択できる汎用表現に関する規則。"""

    class FIELD_001:
        """{{TERM_007}} factory は authoring intent を名前として表してよいが、generic realizer の挙動は factory が明示した literal/template/reference と文書構造上の契約だけに従わなければならない。field 名や値から追加のドメイン意味や presentation を推論してはならない。"""
        merge @= TERMS.TERM_007
        title @= "Explicit field behavior"
        level @= MUST

    class FIELD_002:
        """`field()` は単一または反復する literal 値を compact な inline content として保持し、未参照 field を APPEND する場合は `name: value` を基本形として実現しなければならない。"""
        title @= "Inline field"
        level @= MUST

    class FIELD_003:
        """`list_field()` は各 `@=` 値を同じ field の Markdown bullet list item として実現しなければならない。"""
        title @= "List field"
        level @= MUST

    class FIELD_004:
        """`test_target_field()` は通常のテストから独立して参照・検証したい文字列断片を literal test target として保持しなければならない。Realizer はその値へ fenced code block、language info string、その他の Markdown presentation を暗黙に付加してはならず、template へ参照された位置に正規化済み literal text だけを挿入しなければならない。"""
        title @= "Test target field"
        level @= MUST

    class FIELD_005:
        """`test_target_field()` は作者が通常のテストから直接参照したい断片であることを示すが、その断片に対応するテストが存在すること、またはテストに合格していることを自動保証してはならない。"""
        title @= "Test coverage is not implied"
        level @= MUST_NOT

    class FIELD_006:
        """`test_target_field()` の値をコード、設定、command、expected output などとして文書化する場合、Markdown fence や言語指定などの presentation は docstring または `prose_field` template 側へ記述し、対応する通常のテストから field 値そのものを検証することが望ましい。"""
        title @= "Test-target presentation and verification"
        level @= SHOULD

    class FIELD_007:
        """`table_field()` は宣言された column と同じ幅を持つ各 `@=` row を Markdown table の一行として実現し、row 幅の不一致を validation error としなければならない。"""
        title @= "Table field"
        level @= MUST

    class FIELD_008:
        """`prose_field()` は名前付きの Markdown prose template fragment を保持し、docstring template と同じ {{TERM_013}}、external placeholder、escape 規則で実現しなければならない。"""
        merge @= TERMS.TERM_013
        title @= "Prose field"
        level @= MUST

    class FIELD_009:
        """literal field と `prose_field` の区別は値のドメイン意味ではなく、値を {{TERM_010}} として解釈するか {{TERM_011}} として保持するかを決定する presentation 契約でなければならない。"""
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_011
        title @= "Template-bearing versus literal fields"
        level @= MUST
    class FIELD_010:
        """`reference_field()` は Python object relation を literal text へ平坦化せず semantic reference として保持しなければならない。Markdown realizer は参照元と参照対象の canonical document logical path、および参照対象の rendered heading を解決できる場合、それらから決定論的な relative logical Markdown link を実現し、解決できない値は literal field と同等の安定した表現へ fallback しなければならない。"""
        title @= "Reference field"
        level @= MUST

