"""Context API reference part."""
from shikumi_devdoc.fields.api_reference import detail, input, kind, name, output, related, NAMESPACE, TYPE, VALUE, OPERATION, OTHER, API_NAMESPACE, API_TYPE, API_VALUE, API_OPERATION, API_OTHER
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary

@summary('realization context の保持と解決に関する公開 API。')
@canonical_source('Context', filename='context.md', order=10, merge_policy="all", heading="identity")
class API_REFERENCE_PART:
    """{{TERM_005}} の保持と参照に関するトップレベル公開 API。"""
    merge @= TERMS.TERM_005

    class Context:
        """{{TERM_005}} として与える JSON 互換の外部情報を保持し、ドット区切りキーで解決する値オブジェクト。"""
        merge @= TERMS.TERM_005
        name @= 'shikumi_devdoc.Context'
        kind @= TYPE
        detail @= 'Construction: Mapping から直接構築でき、`Context.from_json()` と `Context.from_mapping()` も利用できる。'

        class from_json:
            """JSON object 文字列から Context を構築する。"""
            name @= 'shikumi_devdoc.Context.from_json'
            kind @= OPERATION
            input @= 'text [str]: JSON object を表す文字列。'
            output @= 'output [Context]: 正規化された Context。'

        class resolve:
            """ドット区切りキーを解決し、Markdown に埋め込める文字列表現を返す。"""
            name @= 'shikumi_devdoc.Context.resolve'
            kind @= OPERATION
            input @= 'key [str]: 例: `project.version`。'
            output @= 'output [str]: 解決した値の文字列表現。'

    class ContextError:
        """Context の構築または参照に失敗したときの基底エラー。"""
        name @= 'shikumi_devdoc.ContextError'
        kind @= TYPE

    class UnknownContextKeyError:
        """存在しない context key を解決しようとしたことを表すエラー。"""
        name @= 'shikumi_devdoc.UnknownContextKeyError'
        kind @= TYPE
