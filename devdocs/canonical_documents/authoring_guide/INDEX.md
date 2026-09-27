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

# shikumi-devdoc Authoring Guide

| Document | Summary |
| --- | --- |
| [Authoring Guide overview](overview.md) | 必要な文書だけを選び、目的文書ごとの推奨パターンから authoring を始めるための総則。 |
| [Writing a README](readme.md) | repository の入口となる README を prose 中心で簡潔に構成する方法。 |
| [Writing a Getting Started guide](getting-started.md) | 初回利用者を一つの成功体験まで案内する task-oriented guide の作り方。 |
| [Writing a Configuration Guide](configuration-guide.md) | 設定ファイルの書き方、発見、合成、出力などを guide として説明する方法。 |
| [Writing CLI documentation](cli-documentation.md) | CLI の基本操作、argument、mode、出力を task-oriented に説明する方法。 |
| [Writing a Specification](specification.md) | 規範的な契約を SPEC_NNN node と specification field set で構造化する方法。 |
| [Writing an API Reference](api-reference.md) | 公開 API を name/kind/input/output/detail と lifecycle field で記述する方法。 |
| [Writing a CHANGELOG](changelog.md) | release 単位の変更履歴を changelog field set で記録し、subject lifecycle と分離する方法。 |
| [Writing a Glossary / Vocabulary](glossary.md) | 共有概念を Vocabulary として定義し、必要な term だけを各 document へ merge する方法。 |
| [Writing Project Status](project-status.md) | 現在状態、方向性、利用者向けnoticeを project status document として記述する方法。 |
| [Building a document collection](collections.md) | 大きな文書を意味領域ごとの独立 canonical document に分け、INDEX を別 realization する方法。 |
| [Advanced authoring decisions](advanced-authoring.md) | 目的別パターンで足りない場合に使う prose/field、identity、reference、context、code example の横断判断。 |
| [LLM authoring workflow](llm-workflow.md) | LLM が目的文書を選び、必要な canonical source だけを変更して検証・再生成するための作業順序。 |
