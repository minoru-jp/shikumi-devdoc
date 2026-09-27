<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/api_reference/__init__.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を公開工程の入力とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# Realizers

意味像を Markdown または Python 参照モジュールへ変換する公開実現 API。

## realizers

実現 API を用途ごとの namespace として公開する。

name: shikumi_devdoc.realizers

kind: Namespace

related: [DIST_008](../specification/distribution.md#dist_008)

### common

Realizer 間で共有する成果物値。

name: shikumi_devdoc.realizers.common

kind: Namespace

#### MarkdownDocument

単一 Markdown 成果物の filename と content を保持する値。

name: shikumi_devdoc.realizers.common.MarkdownDocument

kind: Type

### document

canonical document の実現 API。

name: shikumi_devdoc.realizers.document

kind: Namespace

#### MarkdownRealizer

validated SemanticView に含まれる canonical document root を MarkdownDocument の集合へ実現する realizer。

name: shikumi_devdoc.realizers.document.MarkdownRealizer

kind: Type

input: view [SemanticView]: document system で検証済みの意味像。

output: output [tuple[MarkdownDocument, ...]]: 各 `@canonical_source(..., filename=...)` root の Markdown 成果物。

### index

canonical document collection の索引実現 API。

name: shikumi_devdoc.realizers.index

kind: Namespace

#### IndexMarkdownRealizer

package-level SemanticView に含まれる canonical document metadata から Markdown index を実現する realizer。

name: shikumi_devdoc.realizers.index.IndexMarkdownRealizer

kind: Type

input: view [SemanticView]: document system で package を検証して得た意味像。

output: output [MarkdownDocument]: canonical document title / filename / summary から、文書リンクと概略を列挙する index。

detail: `IndexMarkdownRealizer` は package focus と各 canonical document の `@summary(...)` metadata を要求し、個々の canonical document 本文や canonical source path は索引へ出力しない。

### vocabulary

Vocabulary の実現 API。

name: shikumi_devdoc.realizers.vocabulary

kind: Namespace

#### GlossaryMarkdownRealizer

Vocabulary SemanticView から公開対象用語の Markdown Glossary を実現する realizer。

name: shikumi_devdoc.realizers.vocabulary.GlossaryMarkdownRealizer

kind: Type

### translation

翻訳境界用の実現 API と値。

name: shikumi_devdoc.realizers.translation

kind: Namespace

#### PreserveSpellingTerm

翻訳後も 表記維持 とする Vocabulary term を表す値。

name: shikumi_devdoc.realizers.translation.PreserveSpellingTerm

kind: Type

#### TranslationManifest

翻訳境界を越えて保持する Vocabulary 方針を表す値。

name: shikumi_devdoc.realizers.translation.TranslationManifest

kind: Type

#### translation_manifest

SemanticView から TranslationManifest と診断を収集する操作。

name: shikumi_devdoc.realizers.translation.translation_manifest

kind: Operation

#### SourceRealizer

Markdown realizer を包み、翻訳境界用の機械可読 metadata を付加する realizer。

name: shikumi_devdoc.realizers.translation.SourceRealizer

kind: Type

detail: Scope: 本文の翻訳は行わず、翻訳に必要な意味情報だけを引き渡す。
