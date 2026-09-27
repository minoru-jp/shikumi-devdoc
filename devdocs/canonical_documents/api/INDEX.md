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

# shikumi-devdoc API Reference

| Document | Summary |
| --- | --- |
| [Core](core.md) | トップレベルの公開名前空間と主要エントリポイント。 |
| [Context](context.md) | realization context の保持と解決に関する公開 API。 |
| [Regulations and descriptors](norms.md) | canonical source と文書記述に使う公開 DSL。 |
| [Standard fields](fields.md) | 用途別に再利用できる標準 field set。 |
| [Realizers](realizers.md) | canonical source や語彙を成果物へ変換する公開 realizer API。 |
| [Command-line interface](cli.md) | インストール時に利用できる `shikumi-devdoc` CLI。 |
