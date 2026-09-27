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

# shikumi-devdoc Specification

| Document | Summary |
| --- | --- |
| [Core](core.md) | canonical source と文書体系全体に共通する中核規則。 |
| [Canonical document structure](document.md) | canonical document の node hierarchy、template、local reference に関する規則。 |
| [Vocabulary](vocabulary.md) | 語彙源、参照、公開用語集に関する規則。 |
| [Field presentations](field-presentations.md) | 作者定義 field の汎用 Markdown 表現に関する規則。 |
| [Structured fields](specification.md) | 作者定義 field と自己完結した canonical document に関する規則。 |
| [Domain field vocabularies](api-reference.md) | ドメイン固有記述を標準または作者定義 field で構成する規則。 |
| [Rendering](rendering.md) | Markdown 実現、realization context、canonical document 境界に関する規則。 |
| [Command-line interface](cli.md) | `shikumi-devdoc` CLI の入出力規則。 |
| [Distribution](distribution.md) | wheel に含める文書資産とその位置づけに関する規則。 |
