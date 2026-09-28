"""Domain-field-vocabulary specification part."""

from shikumi_devdoc.fields.specification import MAY, MUST, level
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title


@summary('ドメイン固有記述を標準または作者定義 field で構成する規則。')
@canonical_source("Domain field vocabularies", filename="api-reference.md", order=60, merge_policy="all", heading="identity")
class SPECIFICATION_PART:
    """Specification や API Reference のようなドメイン固有記述を作者定義 field として構成する規則。"""

    class APIREF_001:
        """generic document core は API kind や規範 level のようなドメイン keyword を必須意味論として定義してはならない。{{TERM_009}} が convenience 値を提供する場合でも、作者は独自 {{TERM_007}} / 値で置き換えられなければならない。"""
        merge @= TERMS.TERM_009
        merge @= TERMS.TERM_007
        title @= "Domain keywords belong to authors"
        level @= MUST

    class APIREF_002:
        """API input/output のような情報は作者定義 {{TERM_007}} の値として記述できなければならない。"""
        merge @= TERMS.TERM_007
        title @= "Inputs and outputs as fields"
        level @= MAY

    class APIREF_003:
        """ドメイン固有の補足情報は新しい専用 realizer を要求せず、通常の {{TERM_007}}、prose field、または {{TERM_006}} hierarchy で記述できなければならない。"""
        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_006
        title @= "Generic domain details"
        level @= MUST

    class APIREF_004:
        """ドメイン文書も通常の `@canonical_source(..., filename=...)` document として記述し、専用 root/part 概念を要求してはならない。"""
        title @= "Ordinary canonical documents"
        level @= MUST

    class APIREF_005:
        """ドメイン文書の見出し順序と階層は作者が nested class の配置と入れ子で決定し、realizer が domain kind から再構成してはならない。"""
        title @= "Author-owned document hierarchy"
        level @= MUST

    class APIREF_006:
        """関係情報が必要なドメインは semantic reference を Markdown logical link として実現する標準 `related` field を利用しても、`reference_field(...)` で独自 relation field を定義しても、`field(...)` で literal relation metadata を保持してもよい。generic document core は関係の方向やドメイン意味を規定しない。"""
        merge @= TERMS.TERM_008
        title @= "Relations as field vocabulary"
        level @= MAY

    class APIREF_007:
        """ドメイン専用 realizer は必須ではなく、generic document Markdown realizer だけで情報を失わず {{TERM_002}} を生成できなければならない。"""
        merge @= TERMS.TERM_002
        title @= "Generic realization is sufficient"
        level @= MUST

    class APIREF_008:
        """collection 索引は専用 {{TERM_001}} を二重記述せず、{{TERM_001}} package を入力とする index realizer から派生生成してよい。"""
        merge @= TERMS.TERM_001
        title @= "Collection index is derived from the package"
        level @= MUST

    class APIREF_009:
        """API identity のようなドメイン identity は class nesting または作者定義 field で表現できるが、基盤がその意味を所有してはならない。"""
        title @= "Domain identity is author-owned"
        level @= MUST

    class APIREF_010:
        """Python identifier と異なる公開名が必要な場合は `name = field(\"name\", str)` のような domain field で保持してよい。"""
        title @= "Explicit display names"
        level @= MAY

    class APIREF_011:
        """class nesting は文書階層を意味する。API ownership など追加の意味を同じ nesting に与えるかどうかは domain {{TERM_008}} の作者が決める。"""
        merge @= TERMS.TERM_008
        title @= "Nesting semantics remain author-owned"
        level @= MUST

    class APIREF_012:
        """複数ドメイン文書を束ねるためだけの専用 root entity を基盤へ導入してはならない。"""
        title @= "No domain collection root"
        level @= MUST

    class APIREF_013:
        """`shikumi_devdoc.fields` の {{TERM_009}} は generic field primitives の定義済み組み合わせとして提供してよいが、専用 validator、専用 realizer dispatch、または利用必須のドメイン規則を持ってはならない。"""
        merge @= TERMS.TERM_009
        title @= "Standard fields are conveniences"
        level @= MUST

