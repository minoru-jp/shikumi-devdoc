<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/specification/__init__.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を公開工程の入力とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# Rendering

Markdown 実現、realization context、canonical document 境界に関する規則。

## RENDER_001

標準 Markdown realizer は実現前に `check()` で実現可能性を診断できなければならない。

title: Realization check

level: MUST

## RENDER_002

未知の external placeholder は空文字へ黙って置換せず診断されなければならない。

title: Unknown context reference

level: MUST

condition: canonical document または Glossary を実現する場合。

## RENDER_003

複数ファイルを生成する標準 realizer は、出力 filename と本文を持つ `MarkdownDocument` の集合として成果物を返さなければならない。canonical document の filename は各 root の `@canonical_source(..., filename=...)` 宣言から決定する。

title: Partition output

level: MUST

related: [SPEC_003](specification.md#spec_003)

## RENDER_004

canonical document を後続の翻訳工程へ渡す場合は、Vocabulary の 表記維持 方針を `TranslationSourceRealizer` によって機械可読メタデータとして埋め込んでよい。

title: Translation metadata

level: SHOULD

## RENDER_005

生成物先頭の運用コメントは利用側から明示的に与えられ、realizer がプロジェクト固有文言を自動探索してはならない。

title: Header comments are caller supplied

level: MUST

## RENDER_006

標準 index realizer は document system で package を検証した SemanticView を入力とし、その package tree に含まれる `@canonical_source(...)` canonical source root を収集して一つの Markdown index を生成しなければならない。module focus から collection index を生成してはならない。

title: Package-level collection index

level: MUST

related: [SPEC_009](specification.md#spec_009), [SPEC_011](specification.md#spec_011)

## RENDER_007

標準 index realizer は索引対象となる各 canonical document に `@summary(...)` metadata を要求し、索引には document title へのリンクと summary を提示しなければならない。canonical source path のような作者側の実装詳細を索引本文へ露出してはならない。

title: Index summary metadata

level: MUST

## RENDER_008

標準 document Markdown realizer は nested document node を ATX heading として実現し、semantic reference に使う logical fragment を実際に出力する heading text から決定論的に導出しなければならない。`heading="title"` では解決済み `title @= ...` を見出しに使用し、title がない node は class identity へ fallback する。`heading="identity"` では title の有無にかかわらず class identity を見出しに使用し、title がある場合は human-readable metadata として本文側へ実現する。標準 fragment 変換は GitHub 互換の heading slug 規則を logical reference convention として採用し、heading text を strip・小文字化し、Unicode の英数字・`-`・`_`・空白だけを残した後、連続する空白を `-` へ置換する。これは Markdown 標準による fragment 保証ではなく、downstream renderer が異なる規則を使う場合の調整は publication 側の責務とする。明示 HTML anchor を追加してはならない。

title: Heading-derived logical fragments

level: MUST

## RENDER_009

reference presentation の値が canonical document node を指す場合、標準 document Markdown realizer は参照元と参照先の canonical document logical path から相対 document path を決定し、参照先で実際に出力される heading text から導出した logical fragment と組み合わせて logical Markdown link を生成しなければならない。同一 document 内では fragment-only link を使用してよい。参照先 document が同じ実行で生成されたか、filesystem 上に存在するか、realization の出力 directory、または最終公開先で同じ相対配置になるかを探索・推論してはならない。

title: Logical reference links

level: MUST

related: [CORE_012](core.md#core_012)

## RENDER_010

publication process が canonical document logical path の相対関係、filename、または downstream Markdown renderer の heading-fragment 規則を変更する場合、必要な link rewrite は publication 側の責務としなければならない。その差異を理由に canonical source の semantic relation を Markdown path や fragment へ置き換えてはならない。

title: Publication layout owns link rewrites

level: MUST

## RENDER_011

canonical document root 自体は filename によって semantic reference target にできる。nested canonical document node を `reference_field` の target にする場合、その target を含む root は `heading="identity"` を使用しなければならない。`heading="title"` の nested heading は title、Vocabulary term、context の変更によって fragment が変化し得るため、stable semantic reference target として扱ってはならない。

title: Stable nested reference targets require identity headings

level: MUST
