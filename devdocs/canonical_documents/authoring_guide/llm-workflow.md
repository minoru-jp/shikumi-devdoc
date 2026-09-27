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

# LLM authoring workflow

LLM は作成する文書の目的を先に特定し、その authoring pattern を主な作業指示として使う。

## 最初に必要な文書だけを決める

repository を読んだからといって README、Specification、API Reference、CHANGELOG、Glossary を一式作らない。利用者の目的、既存の公開 surface、保守上必要な契約を確認し、必要な文書だけを選ぶ。

新規作成では [Authoring Guide overview](overview.md) から目的別ページを選ぶ。既存 repository の修正では、まず現在の文書体系と canonical source の境界を読み、既存責務を尊重する。

## 目的別ページを主な指示として使う

Specification を作るなら Specification page、API Reference を作るなら API Reference page の推奨構造から開始する。複数の機能別ページを先にすべて読んで独自の組み合わせを設計しない。

細部の契約が不明なときだけ Specification / API Reference を参照し、特殊な横断判断が必要なときだけ Advanced authoring を読む。

## 生成物ではなく canonical source を編集する

canonical document や published Markdown の表現だけを局所修正せず、対応する canonical source、Vocabulary、realization context へ変更を戻す。validation と realization を通して成果物を再生成し、生成差分を確認する。

## 過剰な構造化を避ける

LLM は規則を見つけるとすべて field 化・Vocabulary 化・分割しやすい。各構造化には validation、再利用、安定 identity、presentation、テスト可能性など具体的な利点を要求し、単なる文章は prose のまま残す。

同じ理由で、文書数を増やすこと自体を改善とみなさない。読者の目的と変更責務が独立するときだけ collection 化する。
