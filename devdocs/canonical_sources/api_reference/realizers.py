"""Realizer API reference part."""

from shikumi_devdoc.fields.api_reference import API_NAMESPACE, OPERATION, TYPE, kind, name, input, output, detail, related
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from devdocs.canonical_sources.specification.distribution import SPECIFICATION_PART as DISTRIBUTION_SPEC


@summary('canonical source や語彙を成果物へ変換する公開 realizer API。')
@canonical_source('Realizers', filename='realizers.md', order=30, placeholders=True, heading="identity")
class API_REFERENCE_PART:
    """意味像を Markdown または Python 参照モジュールへ変換する公開実現 API。"""

    class realizers:
        """実現 API を用途ごとの namespace として公開する。"""
        name @= 'shikumi_devdoc.realizers'
        kind @= API_NAMESPACE
        related @= (DISTRIBUTION_SPEC.DIST_008,)

        class common:
            """Realizer 間で共有する成果物値。"""
            name @= 'shikumi_devdoc.realizers.common'
            kind @= API_NAMESPACE

            class MarkdownDocument:
                """単一 Markdown 成果物の filename と content を保持する値。"""
                name @= 'shikumi_devdoc.realizers.common.MarkdownDocument'
                kind @= TYPE

        class document:
            """{{TERM_002}} の実現 API。"""
            merge @= TERMS.TERM_002
            name @= 'shikumi_devdoc.realizers.document'
            kind @= API_NAMESPACE

            class MarkdownRealizer:
                """validated SemanticView に含まれる {{TERM_002}} root を MarkdownDocument の集合へ実現する realizer。"""
                merge @= TERMS.TERM_002
                name @= 'shikumi_devdoc.realizers.document.MarkdownRealizer'
                kind @= TYPE
                input @= 'view [SemanticView]: document system で検証済みの意味像。'
                output @= 'output [tuple[MarkdownDocument, ...]]: 各 `@canonical_source(..., filename=...)` root の Markdown 成果物。'


        class index:
            """{{TERM_002}} collection の索引実現 API。"""
            merge @= TERMS.TERM_002
            name @= 'shikumi_devdoc.realizers.index'
            kind @= API_NAMESPACE

            class IndexMarkdownRealizer:
                """package-level SemanticView に含まれる {{TERM_002}} metadata から Markdown index を実現する realizer。"""
                merge @= TERMS.TERM_002
                name @= 'shikumi_devdoc.realizers.index.IndexMarkdownRealizer'
                kind @= TYPE
                input @= 'view [SemanticView]: document system で package を検証して得た意味像。'
                output @= 'output [MarkdownDocument]: canonical document title / filename / summary から、文書リンクと概略を列挙する index。'
                detail @= '`IndexMarkdownRealizer` は package focus と各 canonical document の `@summary(...)` metadata を要求し、個々の canonical document 本文や canonical source path は索引へ出力しない。'

        class vocabulary:
            """{{TERM_014}} の実現 API。"""
            merge @= TERMS.TERM_014
            name @= 'shikumi_devdoc.realizers.vocabulary'
            kind @= API_NAMESPACE

            class GlossaryMarkdownRealizer:
                """{{TERM_014}} SemanticView から公開対象用語の Markdown {{TERM_016}} を実現する realizer。"""
                merge @= TERMS.TERM_014
                merge @= TERMS.TERM_016
                name @= 'shikumi_devdoc.realizers.vocabulary.GlossaryMarkdownRealizer'
                kind @= TYPE


        class translation:
            """翻訳境界用の実現 API と値。"""
            name @= 'shikumi_devdoc.realizers.translation'
            kind @= API_NAMESPACE

            class PreserveSpellingTerm:
                """翻訳後も {{TERM_017}} とする {{TERM_015}} を表す値。"""
                merge @= TERMS.TERM_017
                merge @= TERMS.TERM_015
                name @= 'shikumi_devdoc.realizers.translation.PreserveSpellingTerm'
                kind @= TYPE

            class TranslationManifest:
                """翻訳境界を越えて保持する {{TERM_014}} 方針を表す値。"""
                merge @= TERMS.TERM_014
                name @= 'shikumi_devdoc.realizers.translation.TranslationManifest'
                kind @= TYPE

            class translation_manifest:
                """SemanticView から TranslationManifest と診断を収集する操作。"""
                name @= 'shikumi_devdoc.realizers.translation.translation_manifest'
                kind @= OPERATION

            class SourceRealizer:
                """Markdown realizer を包み、翻訳境界用の機械可読 metadata を付加する realizer。"""
                name @= 'shikumi_devdoc.realizers.translation.SourceRealizer'
                kind @= TYPE
                detail @= 'Scope: 本文の翻訳は行わず、翻訳に必要な意味情報だけを引き渡す。'
