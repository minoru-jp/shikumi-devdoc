"""Canonical-document structure specification part."""

from shikumi_devdoc.fields.specification import MAY, MUST, MUST_NOT, SHOULD, level, related
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title
from devdocs.canonical_sources.specification.specification import SPECIFICATION_PART as SPECIFICATION_SPEC


@summary('canonical document の node hierarchy、template、local reference に関する規則。')
@canonical_source("Canonical document structure", filename="document.md", order=10, merge_policy="local", heading="identity")
class SPECIFICATION_PART:
    """canonical document の node hierarchy、template、local reference に関する規則。"""

    class DOC_001:
        """`@canonical_source(...)` root の内部で字句的に定義された class はすべて child {{TERM_006}} として解釈され、その入れ子は canonical Markdown の見出し階層へそのまま写像されなければならない。"""
        merge @= TERMS.TERM_006
        title @= "Nested classes define heading hierarchy"
        level @= MUST

    class DOC_002:
        """canonical root と各 child {{TERM_006}} の docstring は、Python から得た文字列へ `inspect.cleandoc()` 相当の正規化を適用した後、その node の本文 template として扱われなければならない。Python source 上の共通 indent は canonical content に含めず、本文内部の相対 indent は保持しなければならない。"""
        merge @= TERMS.TERM_006
        title @= "Docstrings are templates"
        level @= MUST

    class DOC_003:
        """本文 template 中の raw Markdown heading を意味階層の代替として使用してはならない。文書構造は nested class で表現する。"""
        title @= "Raw Markdown headings"
        level @= MUST_NOT

    class DOC_004:
        """{{TERM_006}} に Python 実体とは別の文字列 anchor identity を定義してはならない。{{TERM_001}} 内の意味参照は、可能な限り Python 実体そのものを利用する。"""
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_001
        title @= "Parallel string node identities"
        level @= MUST_NOT

    class DOC_005:
        """現在版など realization 時点で変化し得る外部値は、{{TERM_001}} へ固定せず {{TERM_012}} と {{TERM_005}} から参照することが望ましい。過去の事実や規範的内容の保存先として context を使用してはならない。"""
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_012
        merge @= TERMS.TERM_005
        title @= "External values"
        level @= SHOULD

    class DOC_006:
        """関係情報は通常の {{TERM_007}} vocabulary として記述してよい。標準 `related` field は評価時点で解決済みの Python class 実体を semantic reference として保持する convenience field であり、generic document core は関係の方向や意味を規定しない。表示の有無と位置は他の {{TERM_007}} と同じ {{TERM_013}} / 未参照 field policy に従わなければならない。"""
        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_013
        title @= "Relations are ordinary fields"
        level @= MAY
        related @= (SPECIFICATION_SPEC.SPEC_008,)

    class DOC_007:
        r"""{{TERM_006}} に field 系 writer で `name @= value` を記述した場合、その左辺 `name` は同じ node の {{TERM_013}} として自動的に利用できなければならない。`merge @= target` は class target の Python identity に基づく参照名を追加し、標準では canonical {{TERM_015}} class を直接 target にできなければならない。文字列、field への別名、その他の明示名には `merge @= ("name", target)` を使用できる。template 内の `\{{name}}` は一意な同一 node の local reference を優先し、該当しない場合だけ {{TERM_012}} として扱う。"""
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_013
        merge @= TERMS.TERM_012
        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_015
        title @= "Unified local references"
        level @= MUST

    class DOC_008:
        """{{TERM_013}} は同じ {{TERM_006}} のみに作用し、親 node、子 node、別 {{TERM_002}} へ暗黙に継承してはならない。field binding、implicit class target、明示 merge alias の参照名が衝突しても登録自体は許可し、template-bearing content が曖昧な参照を実際に使用した場合だけ validation error としなければならない。class target は Vocabulary class 名や module path を含む、より長い一意な Python identity suffix で解決でき、field binding は必要に応じて明示 merge alias で別名を与えられなければならない。未記述 {{TERM_007}} を指す target、未対応 target、`prose_field` を介した local reference cycle は validation error としなければならない。"""
        merge @= TERMS.TERM_013
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_007
        title @= "Merge scope and validation"
        level @= MUST

    class DOC_009:
        r"""{{TERM_010}} では `\{{...}}` によって placeholder marker を literal text として escape できなければならない。`${{...}}` は host-language syntax として literal に保持しなければならない。"""
        merge @= TERMS.TERM_010
        title @= "Template escape"
        level @= MUST

    class DOC_010:
        r"""`field`、`list_field`、`table_field`、`test_target_field` の値は {{TERM_011}} として扱い、内部の `\{{...}}` を placeholder または merge として解釈してはならない。"""
        merge @= TERMS.TERM_011
        title @= "Literal fields stay literal"
        level @= MUST

    class DOC_011:
        """`prose_field` は docstring と同じ template 規則を持つ名前付き本文断片として扱い、{{TERM_012}} と同じ node の {{TERM_013}} を使用できなければならない。"""
        merge @= TERMS.TERM_012
        merge @= TERMS.TERM_013
        title @= "Prose fields are template fragments"
        level @= MUST
    class DOC_012:
        r"""nested {{TERM_006}} の human-readable title は `title @= "..."` によって一つだけ記録しなければならない。`@title(...)` decorator を別の title 記法として提供してはならない。title は docstring / `prose_field` と同じ node-local template namespace を使用でき、同じ node の `merge` と {{TERM_012}} を解決した結果が非空の単一行でなければならない。"""
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_012
        title @= "Unified title information"
        level @= MUST

