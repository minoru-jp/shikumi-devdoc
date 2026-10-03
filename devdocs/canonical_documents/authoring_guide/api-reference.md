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

# Writing an API Reference

API Reference は公開 surface を subject-centered に検索・確認できる形で記録する。

## API Reference を作る場合

Python API、HTTP API、command object など、利用者が個々の公開対象について名前、種別、入力、出力、詳細を調べる必要がある場合に作る。使用手順を教える tutorial ではなく、現在の公開 surface を確認する reference とする。

## API subject を node にする

API entry ごとに node を作り、表示名は `name` field へ置く。cross-reference される API node を持つ document では `@canonical_source(..., heading="identity")` を使用し、class identity に API 名の表記を同期させる必要がない場合は `API_NNN` のような opaque stable identity を使える。package や機能領域が大きい場合は document collection へ分ける。

## 標準 field set を使う

`shikumi_devdoc.fields.api_reference` は `name`、`kind`、`input`、`output`、`detail`、`related` と、`NAMESPACE` / `TYPE` / `VALUE` / `OPERATION` / `OTHER` を提供する。

```python
from shikumi_devdoc.fields.api_reference import OPERATION, input, kind, name, output


class API_001:
    """Process one request and return its result."""

    name @= "run"
    kind @= OPERATION
    input @= "request: Request"
    output @= "RunResult"
```

入出力を文章だけに埋め込むより、一覧や差分で扱う価値がある場合に field として分離する。説明上の背景や例は prose に残してよい。

## Lifecycle を対象のそばに置く

API の導入、非推奨、削除、置換、移行を現在の対象から追える必要がある場合は `shikumi_devdoc.fields.lifecycle` の `introduced`、`deprecated`、`removed`、`replacement`、`migration` を同じ node に付ける。

CHANGELOG は release-centered、lifecycle field は subject-centered であり、同じ変更事実が両方に現れても役割は異なる。
