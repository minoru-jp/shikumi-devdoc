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

# Canonical document structure

canonical document の node hierarchy、template、local reference に関する規則。

## DOC_001

`@canonical_source(...)` root の内部で字句的に定義された class はすべて child document node として解釈され、その入れ子は canonical Markdown の見出し階層へそのまま写像されなければならない。

title: Nested classes define heading hierarchy

level: MUST

## DOC_002

canonical root と各 child document node の docstring は、Python から得た文字列へ `inspect.cleandoc()` 相当の正規化を適用した後、その node の本文 template として扱われなければならない。Python source 上の共通 indent は canonical content に含めず、本文内部の相対 indent は保持しなければならない。

title: Docstrings are templates

level: MUST

## DOC_003

本文 template 中の raw Markdown heading を意味階層の代替として使用してはならない。文書構造は nested class で表現する。

title: Raw Markdown headings

level: MUST NOT

## DOC_004

document node に Python 実体とは別の文字列 anchor identity を定義してはならない。canonical source 内の意味参照は、可能な限り Python 実体そのものを利用する。

title: Parallel string node identities

level: MUST NOT

## DOC_005

現在版など realization 時点で変化し得る外部値は、canonical source へ固定せず external placeholder と realization context から参照することが望ましい。過去の事実や規範的内容の保存先として context を使用してはならない。

title: External values

level: SHOULD

## DOC_006

関係情報は通常の field vocabulary として記述してよい。標準 `related` field は評価時点で解決済みの Python class 実体を semantic reference として保持する convenience field であり、generic document core は関係の方向や意味を規定しない。表示の有無と位置は他の field と同じ local reference / 未参照 field policy に従わなければならない。

title: Relations are ordinary fields

level: MAY

related: [SPEC_008](specification.md#spec_008)

## DOC_007

document node に field 系 writer で `name @= value` を記述した場合、その左辺 `name` は同じ node の local reference として自動的に利用できなければならない。`merge @= target` は class target の Python identity に基づく参照名を追加し、標準では canonical Vocabulary term class を直接 target にできなければならない。文字列、field への別名、その他の明示名には `merge @= ("name", target)` を使用できる。template 内の `{{name}}` は一意な同一 node の local reference を優先し、該当しない場合だけ external placeholder として扱う。

title: Unified local references

level: MUST

## DOC_008

local reference は同じ document node のみに作用し、親 node、子 node、別 canonical document へ暗黙に継承してはならない。field binding、implicit class target、明示 merge alias の参照名が衝突しても登録自体は許可し、template-bearing content が曖昧な参照を実際に使用した場合だけ validation error としなければならない。class target は Vocabulary class 名や module path を含む、より長い一意な Python identity suffix で解決でき、field binding は必要に応じて明示 merge alias で別名を与えられなければならない。未記述 field を指す target、未対応 target、`prose_field` を介した local reference cycle は validation error としなければならない。

title: Merge scope and validation

level: MUST

## DOC_009

template-bearing content では `{{...}}` によって placeholder marker を literal text として escape できなければならない。`${{...}}` は host-language syntax として literal に保持しなければならない。

title: Template escape

level: MUST

## DOC_010

`field`、`list_field`、`table_field`、`test_target_field` の値は literal content として扱い、内部の `{{...}}` を placeholder または merge として解釈してはならない。

title: Literal fields stay literal

level: MUST

## DOC_011

`prose_field` は docstring と同じ template 規則を持つ名前付き本文断片として扱い、external placeholder と同じ node の local reference を使用できなければならない。

title: Prose fields are template fragments

level: MUST

## DOC_012

nested document node の human-readable title は `title @= "..."` によって一つだけ記録しなければならない。`@title(...)` decorator を別の title 記法として提供してはならない。title は docstring / `prose_field` と同じ node-local template namespace を使用でき、同じ node の `merge` と external placeholder を解決した結果が非空の単一行でなければならない。

title: Unified title information

level: MUST
