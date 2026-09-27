<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/api_reference/__init__.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を公開工程の入力とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# Standard fields

Generic field primitives から構成される任意利用の標準 field set。realizer はこれらを特別扱いしない。

## fields

用途別の標準 field、関連定数、helper を公開する convenience namespace。

name: shikumi_devdoc.fields

kind: Namespace

detail: Exports: `shikumi_devdoc.fields.common`, `shikumi_devdoc.fields.specification`, `shikumi_devdoc.fields.api_reference`, `shikumi_devdoc.fields.changelog`, `shikumi_devdoc.fields.lifecycle`, `shikumi_devdoc.fields.status`.

### common

複数の標準 field set で共有する汎用 field definitions。

name: shikumi_devdoc.fields.common

kind: Namespace

detail: Exports: `shikumi_devdoc.fields.common.kind`, `shikumi_devdoc.fields.common.condition`, `shikumi_devdoc.fields.common.detail`, `shikumi_devdoc.fields.common.related`. Node title belongs to `shikumi_devdoc.norms.document.title`.

### specification

仕様書に頻出する field と規範値の標準セット。利用は任意で、generic document core に特別な意味を追加しない。

name: shikumi_devdoc.fields.specification

kind: Namespace

detail: Exports: `shikumi_devdoc.fields.specification.level`, `shikumi_devdoc.fields.specification.condition`, `shikumi_devdoc.fields.specification.detail`, `shikumi_devdoc.fields.specification.related`, `shikumi_devdoc.fields.specification.MUST`, `shikumi_devdoc.fields.specification.MUST_NOT`, `shikumi_devdoc.fields.specification.SHOULD`, `shikumi_devdoc.fields.specification.SHOULD_NOT`, `shikumi_devdoc.fields.specification.MAY`, `shikumi_devdoc.fields.specification.INFORMATIVE`.

### api_reference

API Reference に頻出する field と kind 値の標準セット。

name: shikumi_devdoc.fields.api_reference

kind: Namespace

detail: Exports: `shikumi_devdoc.fields.api_reference.name`, `shikumi_devdoc.fields.api_reference.kind`, `shikumi_devdoc.fields.api_reference.input`, `shikumi_devdoc.fields.api_reference.output`, `shikumi_devdoc.fields.api_reference.detail`, `shikumi_devdoc.fields.api_reference.related`, `shikumi_devdoc.fields.api_reference.NAMESPACE`, `shikumi_devdoc.fields.api_reference.TYPE`, `shikumi_devdoc.fields.api_reference.VALUE`, `shikumi_devdoc.fields.api_reference.OPERATION`, `shikumi_devdoc.fields.api_reference.OTHER`, `shikumi_devdoc.fields.api_reference.API_NAMESPACE`, `shikumi_devdoc.fields.api_reference.API_TYPE`, `shikumi_devdoc.fields.api_reference.API_VALUE`, `shikumi_devdoc.fields.api_reference.API_OPERATION`, `shikumi_devdoc.fields.api_reference.API_OTHER`.

### changelog

CHANGELOG に頻出する release metadata と change-category list field の標準セット。

name: shikumi_devdoc.fields.changelog

kind: Namespace

detail: Exports: `shikumi_devdoc.fields.changelog.version`, `shikumi_devdoc.fields.changelog.released_on`, `shikumi_devdoc.fields.changelog.added`, `shikumi_devdoc.fields.changelog.changed`, `shikumi_devdoc.fields.changelog.deprecated`, `shikumi_devdoc.fields.changelog.removed`, `shikumi_devdoc.fields.changelog.fixed`, `shikumi_devdoc.fields.changelog.security`.

### lifecycle

文書対象の導入・非推奨・削除・置換・移行情報を記録する標準 field set。

name: shikumi_devdoc.fields.lifecycle

kind: Namespace

detail: Exports: `shikumi_devdoc.fields.lifecycle.introduced`, `shikumi_devdoc.fields.lifecycle.deprecated`, `shikumi_devdoc.fields.lifecycle.removed`, `shikumi_devdoc.fields.lifecycle.replacement`, `shikumi_devdoc.fields.lifecycle.migration`.

### status

Project Status に頻出する field と notice kind 値の標準セット。

name: shikumi_devdoc.fields.status

kind: Namespace

detail: Exports: `shikumi_devdoc.fields.status.kind`, `shikumi_devdoc.fields.status.condition`, `shikumi_devdoc.fields.status.related`, `shikumi_devdoc.fields.status.GENERAL`.

### design_contract

標準 field set は generic `field` primitives の定義済み組み合わせであり、専用 validator / realizer dispatch を持たない。

name: standard field-set contract

kind: Value
