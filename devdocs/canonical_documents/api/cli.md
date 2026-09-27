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

# Command-line interface

インストール時に公開される `shikumi-devdoc` コマンド。

## render

canonical source を検証し、canonical Markdown document を生成する。

name: shikumi-devdoc render

kind: Operation

related: [CLI_001](../specification/cli.md#cli_001), [CLI_003](../specification/cli.md#cli_003)

input: kind [document | index | glossary]: 実現する成果物種別。, module [dotted import path]: canonical source module または package。, --output [path]: `document` / `index` では出力ディレクトリ、`glossary` では出力ファイル。

output: output [filesystem artifacts]: 検証と実現に成功した Markdown 成果物。

detail: Optional controls: `--context`、`--notice`、`--translation-source` を利用できる。`render index` では `--index-title` で索引 H1 を指定できる。
