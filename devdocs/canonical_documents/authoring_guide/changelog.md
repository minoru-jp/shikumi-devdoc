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

# Writing a CHANGELOG

CHANGELOG は release-centered な歴史記録として、後から意味が変わらない事実を canonical source に保持する。

## CHANGELOG を作る場合

利用者が release ごとの差分、breaking change、修正内容を追う必要がある場合に作る。内部開発メモだけで十分な project では必須ではない。

## Release を node にする

release ごとに node を作り、`shikumi_devdoc.fields.changelog` の `version`、`released_on`、`added`、`changed`、`deprecated`、`removed`、`fixed`、`security` から必要な field を使う。

```python
from shikumi_devdoc.fields.changelog import added, fixed, version


class V1_2_0:
    """Release 1.2.0."""

    version @= "1.2.0"
    added @= "Added the public `run()` operation."
    fixed @= "Fixed configuration-path resolution."
```

change-category field は literal list content である。`{{...}}` を展開する template として扱わず、歴史記録として残したい文言をそのまま書く。

## Current context と歴史的事実を分ける

現在の project version は realization context に置けるが、過去 release の version や変更内容は canonical source に固定する。再実現したときに過去の CHANGELOG が現在値へ書き換わる設計にしない。CHANGELOG 自体の `@canonical_source(...)` には `merge_policy="forbidden"` を指定し、`merge @= ...` と external context からの差し込みを拒否する。同じ node に直接定義した field の参照はこの policy の対象外なので、release 固有の値を field として固定して本文から参照してもよい。

## Subject lifecycle は対象文書にも残せる

API や設定項目の導入・非推奨・削除を、その対象を読む利用者からも確認させたい場合は lifecycle field を対象自身へ付ける。

```python
introduced @= "0.2.0"
deprecated @= "0.4.0"
replacement @= "new_api"
migration @= "Replace `old_api` with `new_api` when updating callers."
```
