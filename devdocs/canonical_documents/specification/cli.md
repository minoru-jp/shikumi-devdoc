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

# Command-line interface

`shikumi-devdoc` CLI の入出力規則。

## CLI_001

CLI は成果物の出力先を `-o/--output` で利用者から明示的に受け取らなければならない。

title: Explicit output path

level: MUST

## CLI_002

`render document` の `-o` は、`@canonical_source(..., filename=...)` で決まる canonical document を配置する出力ディレクトリとして扱われなければならない。

title: Document output directory

level: MUST

related: [SPEC_003](specification.md#spec_003)

## CLI_003

運用 notice を埋め込む場合は `--notice` で TOML ファイルを明示し、CLI が暗黙に探索してはならない。

title: Notice is explicit

level: MUST

## CLI_004

`render index` は canonical source package を入力として受け取り、その package に含まれる canonical document の索引を `INDEX.md` として指定出力ディレクトリへ生成しなければならない。module 単体は `render index` の入力として受理してはならない。

title: Explicit package index rendering

level: MUST

related: [SPEC_009](specification.md#spec_009)
