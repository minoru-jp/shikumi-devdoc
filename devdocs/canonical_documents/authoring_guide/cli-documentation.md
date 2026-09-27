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

# Writing CLI documentation

CLI documentation は command-line 利用者が目的の操作へ到達するための guide/reference とする。

## CLI documentation を作る場合

command-line interface が主要な公開 surface で、README の最小例だけでは argument、mode、入出力、安全条件を十分に説明できない場合に作る。

## 操作のまとまりで構成する

parser 内部の実装順ではなく、利用者の操作単位で章を分ける。例えば basic invocation、input/target selection、mode、preview/output、exit/error behavior のように、調べる目的が異なるものを分離する。

一枚が長くなる場合は同じ意味領域で collection 化する。単に option 数が多いという理由だけで細かくファイル分割しない。

## Command 例をテスト可能にする

文書に掲載する command は、通常のテストから文字列そのものを検証したい場合に `test_target_field` へ分離する。表示用の `bash` fence は docstring 側に書く。

```bash
example --input src --output build
```

option 名や invocation shape が実装と drift しやすい場合は、parser test または CLI integration test と対応させる。

## 厳密な契約は Specification へ置く

CLI document は「どう使うか」を中心にする。default の決定規則、複数 option の衝突、禁止組み合わせ、exit contract など互換性上の規範は Specification がある場合そちらへ置き、CLI document から対応ページへリンクする。
