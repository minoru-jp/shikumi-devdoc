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

# Distribution

wheel に含める文書資産と、その位置づけに関する規則。

## DIST_001

wheel は `devdocs/` 全体を `shikumi_devdoc/resources/devdocs/` に参照コーパスとして含めなければならない。

title: Installed reference corpus

level: MUST

## DIST_002

wheel は公開 `README.md`、`STATUS.md`、`CHANGELOG.md`、`docs/` を `shikumi_devdoc/resources/published_docs/` に含めなければならない。

title: Installed published documents

level: MUST

## DIST_003

wheel に含める文書資産を `shikumi_devdoc` の importable public API として扱ってはならない。文書資産は package resource として扱う。

title: Documentation resources are not public modules

level: MUST NOT

## DIST_004

MIT License 本文は project metadata の license file として wheel に含め、公開文書資産へ別コピーすることを要求してはならない。

title: License distribution

level: MUST

## DIST_005

sdist からテスト環境を再構築できるよう、テスト用 optional dependency は `pytest` への依存を project metadata に宣言しなければならない。

title: Test dependency metadata

level: MUST

## DIST_006

トップレベル `shikumi_devdoc` は Context 系と `fields` / `norms` / `realizers` 名前空間を公開し、文書記述 DSL や標準 field を flat に再公開してはならない。

title: Small top-level public namespace

level: MUST

## DIST_007

canonical source の基盤記述に必要な公開実体は `shikumi_devdoc.norms.<domain>` に分類しなければならない。canonical source と共通 policy は `shikumi_devdoc.norms.common`、canonical document の field writer と検証 system は `shikumi_devdoc.norms.document` に置く。用途別の standard field set は任意利用の convenience API として `shikumi_devdoc.fields.<domain>` に置いてよいが、generic document core の必須意味論にしてはならない。

title: Namespaced norms authoring surface

level: MUST

## DIST_008

標準 Realizer と公開成果物値は `shikumi_devdoc.realizers.<domain>` に分類し、各 domain 内では `MarkdownRealizer` など文脈上十分な短い名前を利用できなければならない。

title: Namespaced realizer surface

level: MUST
