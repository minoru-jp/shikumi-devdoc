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

# Vocabulary

語彙源、参照、公開用語集に関する規則。

## VOC_001

Vocabulary source は通常の `@canonical_source(...)` root に `@vocabulary` を付与して宣言しなければならない。Vocabulary は独自の文書 grammar を導入してはならない。

title: Vocabulary profile

level: MUST

## VOC_002

Vocabulary root の direct child は Vocabulary term とし、その docstring は `inspect.cleandoc()` 相当の正規化後に `{{term name}}` 宣言で始まらなければならない。term declaration は正規化済み docstring の先頭に一つだけ存在し、宣言 marker の後ろには同一行の本文を置いてはならない。この宣言が term name を設定する唯一の方法である。

title: Term declaration

level: MUST

## VOC_003

term definition は宣言に続く docstring 本文から導出しなければならず、用語名または definition を別 descriptor へ二重記述してはならない。

title: Definition derivation

level: MUST NOT

## VOC_004

Vocabulary term の canonical Python class は、human-facing な用語名とは独立した canonical term identity と用語名・definition を保持し、document node から `merge @= term` の target として直接使用できなければならない。文書側は用語名を別名として再記述せず、term class の Python identity を参照名として利用できなければならない。Vocabulary 全体の接続や別個の reference 宣言を要求してはならない。

title: Term references are merge targets

level: MUST

## VOC_005

Vocabulary の term は既定で Glossary の公開対象として扱わなければならない。`glossary` が未指定または `True` の term は公開し、`glossary @= False` を明示した term だけを除外しなければならない。

title: Public glossary selection

level: MUST

## VOC_006

deprecated 用語の `replacement` は同一 Vocabulary 内の canonical な用語名を指さなければならない。

title: Replacement target

level: MUST

## VOC_007

一つの document node は複数の異なる Vocabulary term を merge target として保持できなければならない。複数の Vocabulary で `TERM_001` のような短い identity が衝突する場合でも、その衝突自体を error としてはならず、`VocabularyA.TERM_001`、さらに必要なら module path を含む Python identity suffix まで伸ばして一意に参照できなければならない。各参照は対応する canonical term name へ独立して実現され、`preserve_spelling` など翻訳に必要な意味情報は merge target の term identity から導出できなければならない。

title: Multiple term merge targets

level: MUST
