"""Norm authoring API reference part."""

from shikumi_devdoc.fields.api_reference import (
    API_NAMESPACE,
    API_OPERATION,
    API_VALUE,
    kind,
    name,
    related,
)
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge as bind, summary
from devdocs.canonical_sources.specification.core import SPECIFICATION_PART as CORE_SPEC
from devdocs.canonical_sources.specification.document import SPECIFICATION_PART as DOCUMENT_SPEC
from devdocs.canonical_sources.specification.distribution import SPECIFICATION_PART as DISTRIBUTION_SPEC


@summary('canonical source と文書記述に使う公開 DSL。')
@canonical_source('Regulations and descriptors', filename='norms.md', order=20, placeholders=True, heading="identity")
class API_REFERENCE_PART:
    """{{TERM_001}} の記述に使う公開 DSL。"""
    bind @= TERMS.TERM_001

    class norms:
        """文書記述 API を意味領域ごとの namespace として公開する。"""
        name @= 'shikumi_devdoc.norms'
        kind @= API_NAMESPACE
        related @= (DISTRIBUTION_SPEC.DIST_007,)

        class common:
            """{{TERM_001}} 間で共有する記述器と {{TERM_002}} policy。"""
            bind @= TERMS.TERM_001
            bind @= TERMS.TERM_002
            name @= 'shikumi_devdoc.norms.common'
            kind @= API_NAMESPACE

            class APPEND:
                """body template から参照されなかった {{TERM_007}} を各 {{TERM_006}} の末尾へ実現する policy 値。"""
                bind @= TERMS.TERM_007
                bind @= TERMS.TERM_006
                name @= 'shikumi_devdoc.norms.common.APPEND'
                kind @= API_VALUE

            class IGNORE:
                """body template から参照されなかった {{TERM_007}} を {{TERM_002}} へ実現しない policy 値。"""
                bind @= TERMS.TERM_007
                bind @= TERMS.TERM_002
                name @= 'shikumi_devdoc.norms.common.IGNORE'
                kind @= API_VALUE

            class canonical_source:
                """{{TERM_001}} unit を宣言する decorator。{{TERM_002}} では root title、filename、`heading="title"|"identity"` の nested heading policy、任意 order、{{TERM_012}} policy、未参照 {{TERM_007}} policy を共通 metadata として宣言する。"""
                bind @= TERMS.TERM_001
                bind @= TERMS.TERM_002
                bind @= TERMS.TERM_012
                bind @= TERMS.TERM_007
                name @= 'shikumi_devdoc.norms.common.canonical_source'
                kind @= API_OPERATION
                related @= (CORE_SPEC.CORE_001, CORE_SPEC.CORE_007)

            class summary:
                """canonical source/document の短い概略 metadata を付与する decorator factory。collection index などの overview realization で利用できる。"""
                name @= 'shikumi_devdoc.norms.common.summary'
                kind @= API_OPERATION

            class merge:
                r"""{{TERM_006}} の local template namespace に参照を追加する writer。class target は `merge @= target` と記述し、Python identity の一意な最短 suffix を参照名として利用できる。標準では {{TERM_015}} の canonical class を直接 target にできる。`merge @= ("name", target)` は明示別名、文字列、同じ node の {{TERM_007}} に利用できる。field 系の `@=` binding は merge なしで {{TERM_013}} に参加する。"""
                bind @= TERMS.TERM_006
                bind @= TERMS.TERM_013
                bind @= TERMS.TERM_007
                bind @= TERMS.TERM_015
                name @= 'shikumi_devdoc.norms.common.merge'
                kind @= API_VALUE

        class document:
            """{{TERM_002}} の共通記述 API。field 系 factory が返す writer は、`@=` 左辺の binding name を同じ node の {{TERM_013}} として自動的に公開する。"""
            bind @= TERMS.TERM_002
            bind @= TERMS.TERM_013
            name @= 'shikumi_devdoc.norms.document'
            kind @= API_NAMESPACE

            class title:
                """nested document node の human-readable title を `title @= "..."` で記録する assignment-only writer。title は同じ node の local merge と realization context を解決でき、heading policy によって visible heading または human-readable metadata として実現される。"""
                name @= 'shikumi_devdoc.norms.document.title'
                kind @= API_VALUE

            class field:
                """literal scalar field writer を作る factory。canonical display name と Python binding name は独立し、`@=` 左辺の binding name は同じ node の local template reference になる。"""
                name @= 'shikumi_devdoc.norms.document.field'
                kind @= API_OPERATION

            class list_field:
                """各 `@=` 値を Markdown bullet list として実現する反復 literal field writer を作る factory。"""
                name @= 'shikumi_devdoc.norms.document.list_field'
                kind @= API_OPERATION

            class reference_field:
                """Python object relation を semantic reference として保持し、解決可能な canonical document node を Markdown logical link として実現する field writer を作る factory。"""
                name @= 'shikumi_devdoc.norms.document.reference_field'
                kind @= API_OPERATION

            class test_target_field:
                """通常のテストから独立して参照・検証したい literal text を分離する field writer を作る factory。Markdown fence や language info string は自動付与せず、presentation は surrounding template に記述する。"""
                name @= 'shikumi_devdoc.norms.document.test_target_field'
                kind @= API_OPERATION

            class table_field:
                """宣言した columns に対応する反復 row を Markdown table として実現する literal field writer を作る factory。"""
                name @= 'shikumi_devdoc.norms.document.table_field'
                kind @= API_OPERATION

            class prose_field:
                """docstring と同じ local reference / external placeholder 規則を持つ名前付き Markdown prose template fragment を作る factory。"""
                name @= 'shikumi_devdoc.norms.document.prose_field'
                kind @= API_OPERATION

            class system:
                """{{TERM_002}} root、nested class node、{{TERM_007}}、local template reference を検証する Shikumi system。"""
                bind @= TERMS.TERM_002
                bind @= TERMS.TERM_007
                name @= 'shikumi_devdoc.norms.document.system'
                kind @= API_VALUE
                related @= (DOCUMENT_SPEC.DOC_001, DOCUMENT_SPEC.DOC_002)

        class vocabulary:
            """通常の {{TERM_001}} に {{TERM_014}} semantic profile を付加する API。"""
            bind @= TERMS.TERM_001
            bind @= TERMS.TERM_014
            name @= 'shikumi_devdoc.norms.vocabulary'
            kind @= API_NAMESPACE

            class vocabulary:
                r"""`@canonical_source(...)` root を {{TERM_014}} として解釈する marker decorator。direct child の docstring を `inspect.cleandoc()` 相当で正規化し、その先頭の `\{{term name}}` 宣言から term name と definition を導出する。"""
                bind @= TERMS.TERM_014
                name @= 'shikumi_devdoc.norms.vocabulary.vocabulary'
                kind @= API_OPERATION

            class preserve_spelling:
                """term の {{TERM_017}} を `@=` で宣言する writer。"""
                bind @= TERMS.TERM_017
                name @= 'shikumi_devdoc.norms.vocabulary.preserve_spelling'
                kind @= API_VALUE

            class glossary:
                """term の {{TERM_016}} 公開選択を `@=` で上書きする writer。未指定時は公開され、`False` で除外する。"""
                bind @= TERMS.TERM_016
                name @= 'shikumi_devdoc.norms.vocabulary.glossary'
                kind @= API_VALUE

            class alias:
                """term の別名を `@=` で追加する writer。"""
                name @= 'shikumi_devdoc.norms.vocabulary.alias'
                kind @= API_VALUE

            class deprecated:
                """term が廃止済みであることを `@=` で宣言する writer。"""
                name @= 'shikumi_devdoc.norms.vocabulary.deprecated'
                kind @= API_VALUE

            class replacement:
                """廃止済み term の置換先 canonical name を `@=` で宣言する writer。"""
                name @= 'shikumi_devdoc.norms.vocabulary.replacement'
                kind @= API_VALUE

            class system:
                """{{TERM_014}} を検証する Shikumi system。"""
                bind @= TERMS.TERM_014
                name @= 'shikumi_devdoc.norms.vocabulary.system'
                kind @= API_VALUE
