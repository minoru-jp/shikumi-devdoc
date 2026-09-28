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

# Core

文書体系全体に共通する中核規則。

## CORE_001

canonical document を構成する権威ある各文書ソース単位は `@canonical_source` によって明示されなければならない。bare `@canonical_source` は Vocabulary のような非文書 canonical source にも使用できる。

title: Canonical source

level: MUST

## CORE_002

標準 realizer へ渡す意味像は、対応する規定体による検証に成功していなければならない。

title: Validate before realization

level: MUST

## CORE_003

README は入口、Project Status は現在と現在から見た未来、Specification は現行規則、API Reference は公開インターフェース、CHANGELOG は過去の変更を担当する。これらは `shikumi-devdoc` の専用文書型ではなく、利用側が共通 document model 上に構成するドメイン文書であってよい。

title: Public documentation roles

level: INFORMATIVE

## CORE_004

canonical document は、canonical source を対応する規定体で検証し、必要な realization context を注入し、realizer によって文書として組み立てた結果である。`shikumi-devdoc` が一貫して扱う文書成果物の責務境界は canonical document までとする。

title: Canonical document

level: INFORMATIVE

## CORE_005

realization context は、現在版など canonical source に固定せず実現時点で外部から与える値の入力である。Context は歴史的事実の保存先や、canonical source の代替となる正本を意味しない。

title: Realization context

level: INFORMATIVE

## CORE_006

published document は canonical document から翻訳、ローカライズ、表現調整、媒体変換、配布などの公開工程で作られる派生物である。これらの publication workflow は利用側の事情に依存し、`shikumi-devdoc` は特定の公開方法を規定しない。

title: Published document boundary

level: INFORMATIVE

## CORE_007

`@canonical_source` が記録する canonical source の出自は、その Python module の構造から安定して決定され、プロセスの current working directory に依存してはならない。

title: Canonical source provenance

level: MUST

## CORE_008

canonical document の root title、filename、nested heading policy、任意 order、merge policy、未参照 field policy は文書内容の意味論から独立した共通 metadata として `@canonical_source(...)` に宣言されなければならない。nested heading policy は `heading="title"` または `heading="identity"` のどちらかを作者が明示し、realizer が文書種別から推論してはならない。

title: Canonical document metadata

level: MUST

## CORE_009

canonical document は単一の document node model を使用しなければならない。root と nested class は同じ node model を共有し、docstring template、作者定義 field、nested class hierarchy の組合せによって文書を構成しなければならない。

title: Unified canonical document model

level: MUST

## CORE_010

`@canonical_source(..., merge_policy=...)` は template-bearing content が参照できる値の出所を `"all"`、`"local"`、`"external"`、`"forbidden"` の4段階で制御しなければならない。`"all"` は local reference と external placeholder の双方を許可し、`"local"` は local reference だけ、`"external"` は external placeholder だけを許可し、`"forbidden"` は双方を禁止する。未指定時は `"all"` とする。

title: Merge policy

level: MUST

## CORE_010A

`merge_policy="external"` または `merge_policy="forbidden"` の canonical document は、使用の有無にかかわらず `merge @= ...` 宣言を持ってはならず、field binding を含む local reference を template-bearing content から参照してはならない。通常の field value は literal content として保持でき、その内部の placeholder-like text は template 解釈してはならない。

title: Local merge prohibition

level: MUST

## CORE_010B

非推奨の `placeholders=True` は `merge_policy="all"`、`placeholders=False` は `merge_policy="local"` と等価に解釈されなければならない。`placeholders` と `merge_policy` を同時指定してはならない。`placeholders` の使用は API 直接利用時にも deprecation warning を送出し、CLI 利用時にはその warning が利用者へ表示されなければならない。`placeholders` は 1.0.0 で削除予定とする。

title: Legacy placeholders compatibility

level: MUST

## CORE_011

`unreferenced_fields=APPEND` は template から参照されなかった field を各 document node の末尾へ実現し、`unreferenced_fields=IGNORE` はそれらを canonical source 上の情報として保持したまま canonical document へ出力しない policy でなければならない。

title: Unreferenced field policy

level: MUST

## CORE_012

canonical document の logical path は、`CanonicalSource` が記録する Python module provenance の親 path と、root に宣言された canonical filename の組合せから決定論的に導出されなければならない。この logical path は canonical document体系上の出自と相対配置を表し、realization の出力 directory や published document の配置を表してはならない。

title: Canonical document logical path

level: MUST
