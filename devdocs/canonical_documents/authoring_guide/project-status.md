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

# Writing Project Status

Project Status は release history ではなく、現在時点の状態と将来方向を説明する。

## Project Status を作る場合

Beta、experimental、maintenance-only など現在の成熟度、互換性方針、既知の移行予定を README より詳しく伝える必要がある場合に作る。安定状態で特別な告知がない project では不要なことも多い。

## 現在事実と将来方向を分ける

現在の状態、将来の方向、特定条件での notice を同じ prose に混ぜない。`shikumi_devdoc.fields.status` の `kind`、`condition`、`related` と、`shikumi_devdoc.norms.document.title` は必要な意味だけを構造化するために利用できる。

## CHANGELOG の代わりにしない

Project Status は現在像を説明し、CHANGELOG は release ごとの過去事実を記録する。状態が変化した場合、現在文書は更新してよいが、過去 release の変更事実は CHANGELOG に残す。
