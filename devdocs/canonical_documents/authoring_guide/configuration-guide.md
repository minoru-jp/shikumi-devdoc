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

# Writing a Configuration Guide

Configuration Guide は設定を作成する利用者の作業順序と概念理解を支援する。

## Configuration Guide を作る場合

project が設定ファイル、宣言的 schema、複数 source の合成などを公開し、README の断片だけでは安全に使えない場合に作る。設定が数個の単純な値だけなら README や API Reference だけで十分な場合もある。

## 利用者の判断単位で構成する

syntax の列挙だけでなく、利用者がどの設定をどこに置き、どう選択され、どう組み合わされ、どこへ影響するかを説明する。大きくなった場合は discovery、schema/reference、selection、composition、output、examples など意味領域ごとの document collection へ分ける。

## 検証対象の設定例だけ test_target_field に分離する

TOML、YAML、JSON などの設定例は、parse や schema validation で値そのものを検証したい場合だけ `test_target_field` とする。通常の小さな例は docstring の fenced block に直接書いてよい。

```toml
[tool.example]
enabled = true
```

`test_target_field` は Markdown fence を自動生成せず、テスト済みであることも自動保証しない。fence は docstring 側に書き、対応する parser や project の設定 loader を通常のテストから実行する。

## Guide と Specification を分ける

Guide では「どう設定すればよいか」を説明し、値の優先順位、衝突、path 解決、禁止条件など実装が従う厳密な契約がある場合は Specification に置く。Guide からは対応する specification document へリンクし、規則本文を丸ごと複製しない。
