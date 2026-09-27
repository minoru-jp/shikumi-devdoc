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

# Domain field vocabularies

Specification や API Reference のようなドメイン固有記述を作者定義 field として構成する規則。

## APIREF_001

generic document core は API kind や規範 level のようなドメイン keyword を必須意味論として定義してはならない。standard field set が convenience 値を提供する場合でも、作者は独自 field / 値で置き換えられなければならない。

title: Domain keywords belong to authors

level: MUST

## APIREF_002

API input/output のような情報は作者定義 field の値として記述できなければならない。

title: Inputs and outputs as fields

level: MAY

## APIREF_003

ドメイン固有の補足情報は新しい専用 realizer を要求せず、通常の field、prose field、または document node hierarchy で記述できなければならない。

title: Generic domain details

level: MUST

## APIREF_004

ドメイン文書も通常の `@canonical_source(..., filename=...)` document として記述し、専用 root/part 概念を要求してはならない。

title: Ordinary canonical documents

level: MUST

## APIREF_005

ドメイン文書の見出し順序と階層は作者が nested class の配置と入れ子で決定し、realizer が domain kind から再構成してはならない。

title: Author-owned document hierarchy

level: MUST

## APIREF_006

関係情報が必要なドメインは semantic reference を Markdown logical link として実現する標準 `related` field を利用しても、`reference_field(...)` で独自 relation field を定義しても、`field(...)` で literal relation metadata を保持してもよい。generic document core は関係の方向やドメイン意味を規定しない。

title: Relations as field vocabulary

level: MAY

## APIREF_007

ドメイン専用 realizer は必須ではなく、generic document Markdown realizer だけで情報を失わず canonical document を生成できなければならない。

title: Generic realization is sufficient

level: MUST

## APIREF_008

collection 索引は専用 canonical source を二重記述せず、canonical source package を入力とする index realizer から派生生成してよい。

title: Collection index is derived from the package

level: MUST

## APIREF_009

API identity のようなドメイン identity は class nesting または作者定義 field で表現できるが、基盤がその意味を所有してはならない。

title: Domain identity is author-owned

level: MUST

## APIREF_010

Python identifier と異なる公開名が必要な場合は `name = field("name", str)` のような domain field で保持してよい。

title: Explicit display names

level: MAY

## APIREF_011

class nesting は文書階層を意味する。API ownership など追加の意味を同じ nesting に与えるかどうかは domain field vocabulary の作者が決める。

title: Nesting semantics remain author-owned

level: MUST

## APIREF_012

複数ドメイン文書を束ねるためだけの専用 root entity を基盤へ導入してはならない。

title: No domain collection root

level: MUST

## APIREF_013

`shikumi_devdoc.fields` の standard field set は generic field primitives の定義済み組み合わせとして提供してよいが、専用 validator、専用 realizer dispatch、または利用必須のドメイン規則を持ってはならない。

title: Standard fields are conveniences

level: MUST
