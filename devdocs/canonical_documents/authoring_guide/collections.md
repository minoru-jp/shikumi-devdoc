<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/authoring_guide/__init__.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を公開工程の入力とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# Building a document collection

Collection は、独立して読めて独立して変更できる canonical document の集合として構成する。

## Collection を作る場合

一つの文書が長いという理由だけではなく、意味領域ごとに変更責務、参照先、読者の目的が独立してきた場合に collection 化する。Specification、API Reference、Configuration Guide、CLI documentation などは collection に育ちやすい。

小さい文書を形式的に分割しない。読者が全ページを順番に読まなければ意味が成立しない場合は、一枚の document の方が自然なこともある。

## 各 document を独立した canonical source にする

collection 全体の専用 grammar を作るのではなく、各ページをそれぞれ `@canonical_source(...)` root とする。各 document は単独で validation / realization できる状態を保つ。

```text
canonical_sources/
  specification/
    __init__.py
    overview.py
    paths.py
    output.py
```

## 順序と summary を metadata にする

人間向けに安定順が必要なら `@canonical_source(..., order=...)` を指定し、INDEX で各文書の役割を示したい場合は `@summary(...)` を付ける。order は文書内容の identity ではなく collection presentation のための metadata として扱う。

## INDEX は別 realization にする

individual document と collection index の生成を分ける。document realizer に暗黙の `INDEX.md` 生成を持たせず、`render index` / `IndexMarkdownRealizer` で collection package から index を生成する。

公開工程で翻訳する場合も、INDEX だけに canonical source にない説明を追加せず、各 document の `@summary(...)` に戻して正本を更新する。
