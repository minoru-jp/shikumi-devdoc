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

# Regulations and descriptors

canonical source の記述に使う公開 DSL。

## norms

文書記述 API を意味領域ごとの namespace として公開する。

name: shikumi_devdoc.norms

kind: Namespace

related: [DIST_007](../specification/distribution.md#dist_007)

### common

canonical source 間で共有する記述器と canonical document policy。

name: shikumi_devdoc.norms.common

kind: Namespace

#### APPEND

body template から参照されなかった field を各 document node の末尾へ実現する policy 値。

name: shikumi_devdoc.norms.common.APPEND

kind: Value

#### IGNORE

body template から参照されなかった field を canonical document へ実現しない policy 値。

name: shikumi_devdoc.norms.common.IGNORE

kind: Value

#### canonical_source

canonical source unit を宣言する decorator。canonical document では root title、filename、`heading="title"|"identity"` の nested heading policy、任意 order、external placeholder policy、未参照 field policy を共通 metadata として宣言する。

name: shikumi_devdoc.norms.common.canonical_source

kind: Operation

related: [CORE_001](../specification/core.md#core_001), [CORE_007](../specification/core.md#core_007)

#### summary

canonical source/document の短い概略 metadata を付与する decorator factory。collection index などの overview realization で利用できる。

name: shikumi_devdoc.norms.common.summary

kind: Operation

#### merge

document node の local template namespace に参照を追加する writer。class target は `merge @= target` と記述し、Python identity の一意な最短 suffix を参照名として利用できる。標準では Vocabulary term の canonical class を直接 target にできる。`merge @= ("name", target)` は明示別名、文字列、同じ node の field に利用できる。field 系の `@=` binding は merge なしで local reference に参加する。

name: shikumi_devdoc.norms.common.merge

kind: Value

### document

canonical document の共通記述 API。field 系 factory が返す writer は、`@=` 左辺の binding name を同じ node の local reference として自動的に公開する。

name: shikumi_devdoc.norms.document

kind: Namespace

#### title

nested document node の human-readable title を `title @= "..."` で記録する assignment-only writer。title は同じ node の local merge と realization context を解決でき、heading policy によって visible heading または human-readable metadata として実現される。

name: shikumi_devdoc.norms.document.title

kind: Value

#### field

literal scalar field writer を作る factory。canonical display name と Python binding name は独立し、`@=` 左辺の binding name は同じ node の local template reference になる。

name: shikumi_devdoc.norms.document.field

kind: Operation

#### list_field

各 `@=` 値を Markdown bullet list として実現する反復 literal field writer を作る factory。

name: shikumi_devdoc.norms.document.list_field

kind: Operation

#### reference_field

Python object relation を semantic reference として保持し、解決可能な canonical document node を Markdown logical link として実現する field writer を作る factory。

name: shikumi_devdoc.norms.document.reference_field

kind: Operation

#### test_target_field

通常のテストから独立して参照・検証したい literal text を分離する field writer を作る factory。Markdown fence や language info string は自動付与せず、presentation は surrounding template に記述する。

name: shikumi_devdoc.norms.document.test_target_field

kind: Operation

#### table_field

宣言した columns に対応する反復 row を Markdown table として実現する literal field writer を作る factory。

name: shikumi_devdoc.norms.document.table_field

kind: Operation

#### prose_field

docstring と同じ local reference / external placeholder 規則を持つ名前付き Markdown prose template fragment を作る factory。

name: shikumi_devdoc.norms.document.prose_field

kind: Operation

#### system

canonical document root、nested class node、field、local template reference を検証する Shikumi system。

name: shikumi_devdoc.norms.document.system

kind: Value

related: [DOC_001](../specification/document.md#doc_001), [DOC_002](../specification/document.md#doc_002)

### vocabulary

通常の canonical source に Vocabulary semantic profile を付加する API。

name: shikumi_devdoc.norms.vocabulary

kind: Namespace

#### vocabulary

`@canonical_source(...)` root を Vocabulary として解釈する marker decorator。direct child の docstring を `inspect.cleandoc()` 相当で正規化し、その先頭の `{{term name}}` 宣言から term name と definition を導出する。

name: shikumi_devdoc.norms.vocabulary.vocabulary

kind: Operation

#### preserve_spelling

term の 表記維持 を `@=` で宣言する writer。

name: shikumi_devdoc.norms.vocabulary.preserve_spelling

kind: Value

#### glossary

term の Glossary 公開選択を `@=` で上書きする writer。未指定時は公開され、`False` で除外する。

name: shikumi_devdoc.norms.vocabulary.glossary

kind: Value

#### alias

term の別名を `@=` で追加する writer。

name: shikumi_devdoc.norms.vocabulary.alias

kind: Value

#### deprecated

term が廃止済みであることを `@=` で宣言する writer。

name: shikumi_devdoc.norms.vocabulary.deprecated

kind: Value

#### replacement

廃止済み term の置換先 canonical name を `@=` で宣言する writer。

name: shikumi_devdoc.norms.vocabulary.replacement

kind: Value

#### system

Vocabulary を検証する Shikumi system。

name: shikumi_devdoc.norms.vocabulary.system

kind: Value
