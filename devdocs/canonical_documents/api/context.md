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

# Context

realization context の保持と参照に関するトップレベル公開 API。

## Context

realization context として与える JSON 互換の外部情報を保持し、ドット区切りキーで解決する値オブジェクト。

name: shikumi_devdoc.Context

kind: Type

detail: Construction: Mapping から直接構築でき、`Context.from_json()` と `Context.from_mapping()` も利用できる。

### from_json

JSON object 文字列から Context を構築する。

name: shikumi_devdoc.Context.from_json

kind: Operation

input: text [str]: JSON object を表す文字列。

output: output [Context]: 正規化された Context。

### resolve

ドット区切りキーを解決し、Markdown に埋め込める文字列表現を返す。

name: shikumi_devdoc.Context.resolve

kind: Operation

input: key [str]: 例: `project.version`。

output: output [str]: 解決した値の文字列表現。

## ContextError

Context の構築または参照に失敗したときの基底エラー。

name: shikumi_devdoc.ContextError

kind: Type

## UnknownContextKeyError

存在しない context key を解決しようとしたことを表すエラー。

name: shikumi_devdoc.UnknownContextKeyError

kind: Type
