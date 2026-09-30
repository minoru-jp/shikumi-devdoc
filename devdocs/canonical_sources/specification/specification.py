"""Structured-field specification part."""

from shikumi_devdoc.fields.specification import MAY, MUST, condition, level
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title


@summary('作者定義 field と自己完結した canonical document に関する規則。')
@canonical_source("Structured fields", filename="specification.md", order=50, merge_policy="local", heading="identity")
class SPECIFICATION_PART:
    """作者定義 field と自己完結した canonical document に関する規則。"""

    class SPEC_001:
        """canonical root の内部で字句的に定義された class は {{TERM_006}} として解釈され、その identity は Python クラス名と class の入れ子から導出されなければならない。個々の node に専用 decorator を要求してはならない。"""
        merge @= TERMS.TERM_006
        title @= "Class-derived document-node identity"
        level @= MUST

    class SPEC_002:
        """`field(name, value_type, ...)` などが宣言する canonical display name と Python 上で writer を保持する変数名、および `@=` を記述する左辺 binding name は独立でなければならない。"""
        title @= "Author-defined field names"
        level @= MUST

    class SPEC_003:
        """各 {{TERM_002}} は `@canonical_source(..., filename=...)` に自身が生成する Markdown の filename を明示し、それ単独で検証・実現可能でなければならない。"""
        merge @= TERMS.TERM_002
        title @= "Self-contained document filename"
        level @= MUST

    class SPEC_004:
        """`@canonical_source(..., order=...)` は複数文書を安定順で扱いたい場合だけ指定してよい。"""
        title @= "Optional document order"
        level @= MAY

    class SPEC_005:
        """{{TERM_006}} の入れ子は canonical Markdown の見出し入れ子そのものとして解釈しなければならない。Markdown で表現できない深度は realization check で拒否する。"""
        merge @= TERMS.TERM_006
        title @= "Node nesting is heading nesting"
        level @= MUST
        condition @= "Markdown へ実現する場合。"

    class SPEC_006:
        """未参照 field を自動実現する場合でも、field name だけを根拠に Markdown heading へ昇格させてはならない。field presentation は field factory が宣言する文書構造に従う。"""
        title @= "Fields are not headings"
        level @= MUST

    class SPEC_007:
        """Specification、API Reference、ADR などのドメイン {{TERM_008}} は `field()` などの writer の組として利用側または別ライブラリで定義できなければならない。"""
        merge @= TERMS.TERM_008
        title @= "External domain field vocabularies"
        level @= MUST

    class SPEC_008:
        """field value として Python class を使用する場合、その実体は評価時点で解決済みでなければならない。基盤は文字列 ID、forward reference、symbolic reference の解決機構を追加しない。"""
        title @= "Direct Python references"
        level @= MUST

    class SPEC_009:
        """個別 {{TERM_002}} の実現と collection index の実現は独立した操作でなければならない。標準 document realizer は `INDEX.md` を暗黙生成せず、index realizer は明示的に指定された package の {{TERM_001}} 集合から索引だけを生成する。"""
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_001
        title @= "Separate document and index realization"
        level @= MUST

    class SPEC_010:
        """realizer は {{TERM_006}} hierarchy をドメイン意味から再編集せず、作者が記述した class hierarchy をそのまま Markdown heading hierarchy へ写像しなければならない。"""
        merge @= TERMS.TERM_006
        title @= "Preserve author hierarchy"
        level @= MUST

    class SPEC_011:
        """複数の {{TERM_002}} は共通 root entity への依存を持たず、それぞれ独立した `@canonical_source(...)` root の集合として扱われなければならない。"""
        merge @= TERMS.TERM_002
        title @= "No collection-root dependency"
        level @= MUST
