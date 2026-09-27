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

# Writing a Getting Started guide

Getting Started は reference ではなく、最短の成功経路を順番に案内する。

## Getting Started を作る場合

README の最小例だけでは初回利用に必要な手順を説明しきれない場合に作る。読者が installation から一つの成功結果まで順番に進むための文書であり、全機能を網羅する reference ではない。

## 一つの happy path を選ぶ

最も一般的で依存関係の少ない利用経路を一つ選び、前提条件、installation、最小設定、実行、期待結果の順に記述する。途中で複数の選択肢を大量に提示せず、代替手段は成功後の「次に読む文書」へ送る。

## 実行可能な例を優先する

command、Python snippet、設定例などを通常のテストから直接検証したい場合だけ `test_target_field` に分離する。表示用の Markdown fence は docstring 側に書き、通常のテストスイートで field 値そのものを検証する。

```bash
example --help
```

## Reference を複製しない

Getting Started では、その手順に必要な設定や option だけを説明する。完全な設定一覧は Configuration Guide、完全な option 一覧は CLI documentation、契約上の例外条件は Specification へリンクする。
