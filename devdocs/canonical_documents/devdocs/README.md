<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/workspace/canonical.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を公開工程の入力とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# devdocs/

`devdocs/` は、このリポジトリ自身の文書体系をドッグフーディングするためのオーサリング・ワークスペースである。

ここでは、Python で記述する canonical source、実現時に注入する realization context、そこから生成される canonical document を明示的に分離する。canonical document から翻訳・ローカライズ・配布などを経て作る published document は、このライブラリ固有の責務ではなく、このリポジトリの公開運用としてトップレベルの `README.md`、`STATUS.md`、`CHANGELOG.md`、および `docs/` に配置する。

## ディレクトリ構成

```text
devdocs/
├── README.md
├── canonical_sources/
├── config/
│   ├── context.json
│   └── notice.toml
└── canonical_documents/
```

- `canonical_sources/` は、canonical document を構成する権威ある Python canonical source 単位を保持する。
- Specification / API Reference / STATUS / CHANGELOG の field set は `shikumi_devdoc.fields` の standard field set を dogfood する。
- `config/` は、realization context や生成 notice など、このリポジトリ固有の実現時入力を保持する。
- `canonical_documents/` は、canonical source を検証し、必要な context を注入して realizer で組み立てた canonical document を保持する。
- `README.md` はこのワークスペースの入口であり、このファイル自身も `canonical_sources/workspace/canonical.py` から canonical document を生成し、その公開版として配置する。

## Canonical source

`canonical_sources/` の Python 記述体は、canonical document を生成するための権威ある canonical source である。README、Authoring Guide、Project Status、CHANGELOG、Specification、API Reference、Vocabulary、およびこの `devdocs/README.md` の source unit をここに置く。

README、Authoring Guide、STATUS、CHANGELOG、Specification、API Reference はいずれも共通の `@canonical_source(...)` document model で記述する。Specification と API Reference は専用の root / part 規定体を持たず、各ファイルを独立した canonical document とする。collection の `INDEX.md` は canonical source を二重記述せず、package を入力とする独立した index realizer から生成し、各文書の `@summary(...)` metadata を概略として利用する。

canonical source では `shikumi_devdoc.norms` の基盤 API と、必要に応じて `shikumi_devdoc.fields` の standard field set を import する。canonical source と共通 policy は `norms.common`、document field writer と検証 system は `norms.document` を利用する。standard field set は generic primitives の定義済み組み合わせにすぎず、独自 field vocabulary へ置き換えられる。Norm の実装モジュールは private であり、作例でも公開 import path として使用しない。標準文書実現器は `shikumi_devdoc.realizers.document` から利用する。

Vocabulary の意味上の正本は `canonical_sources/vocabulary/canonical.py` に保持される。Vocabulary source 自体も通常の `@canonical_source(...)` であり、`@vocabulary` marker が semantic profile を付与する。各 direct child の docstring は共通 indent を正規化した後、先頭の `{{term name}}` 宣言から用語名を定義し、その後続本文を definition とする。Vocabulary term はこの canonical class を直接参照するため、IDE 向け proxy module は生成しない。

## Realization context

`config/context.json` は、プロジェクト名、現在版、対象 Python 版など、canonical source に固定せず realization 時点で外部から注入する値を保持する realization context である。このファイルは `shikumi-devdoc` の一般仕様ではなく、このリポジトリの運用上の入力である。

Context は歴史的事実の保存先ではない。例えば CHANGELOG の過去バージョンのように後から変化してはならない情報は canonical source に直接記述する。一方、README の現在バージョンのように realization 時点の値を反映したい情報は context に置ける。

`config/notice.toml` は、canonical document の先頭へ埋め込む生成上の注意事項と、後続の翻訳・公開工程に渡すこのリポジトリ固有の方針を保持する。

CLI はこれらのファイルを自動探索しない。`context.json` は JSON 文字列として `--context` へ渡し、`notice.toml` は `--notice` で明示的に指定する。

## Canonical document

`canonical_documents/` は `shikumi-devdoc` が一貫して責任を持つ成果物の境界である。canonical source を対応する規定体で検証し、realization context を注入し、realizer によって文書として組み立てた結果を canonical document とする。

canonical document は生成物だが、単なる一時ファイルではない。この時点で文書としての内容が確定しており、規定体が意図どおり実現されたか、context が正しく反映されたか、翻訳前の日本語が適切かを確認する境界面として Git に保持する。

canonical document は直接編集しない。変更が必要な場合は `canonical_sources/` または realization context へ戻って修正し、再生成する。

## 生成

リポジトリルートから、次のように canonical document を再生成できる。

```bash
CONTEXT="$(cat devdocs/config/context.json)"

shikumi-devdoc render glossary \
  devdocs.canonical_sources.vocabulary.canonical \
  -o devdocs/canonical_documents/GLOSSARY.md \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.readme.canonical \
  -o devdocs/canonical_documents \
  --context "$CONTEXT" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.authoring_guide \
  -o devdocs/canonical_documents/authoring_guide \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render index \
  devdocs.canonical_sources.authoring_guide \
  -o devdocs/canonical_documents/authoring_guide \
  --index-title "shikumi-devdoc Authoring Guide" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.workspace.canonical \
  -o devdocs/canonical_documents/devdocs \
  --notice devdocs/config/notice.toml

shikumi-devdoc render document \
  devdocs.canonical_sources.status.canonical \
  -o devdocs/canonical_documents \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.changelog.canonical \
  -o devdocs/canonical_documents/changelog \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.specification \
  -o devdocs/canonical_documents/specification \
  --context "$CONTEXT" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render index \
  devdocs.canonical_sources.specification \
  -o devdocs/canonical_documents/specification \
  --context "$CONTEXT" \
  --index-title "shikumi-devdoc Specification" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render document \
  devdocs.canonical_sources.api_reference \
  -o devdocs/canonical_documents/api \
  --context "$CONTEXT" \
  --notice devdocs/config/notice.toml \
  --translation-source

shikumi-devdoc render index \
  devdocs.canonical_sources.api_reference \
  -o devdocs/canonical_documents/api \
  --context "$CONTEXT" \
  --index-title "shikumi-devdoc API Reference" \
  --notice devdocs/config/notice.toml \
  --translation-source
```

`merge_policy` は local merge と external context の許可範囲を `"all"` / `"local"` / `"external"` / `"forbidden"` で宣言する。このリポジトリでは CHANGELOG を `"forbidden"` とし、過去の記録が後の local/external 値変更で変化しないようにする。TRUST 型の自己完結文書に相当する文書や Authoring Guide、STATUS、`devdocs/README.md` は必要に応じて `"local"` を使い、README、Specification、API Reference は外部 context が必要な箇所で `"all"` を使う。旧 `placeholders` は 0.3.2 から非推奨である。

## テスト

sdist からテスト環境を再構築する場合は、テスト用 optional dependency をインストールする。

```bash
python -m pip install '.[test]'
pytest
```

`test` extra は `pytest>=8.0` を宣言する。pytest は通常利用時の必須依存には含めない。

公開前の distribution verification は hosted CI に依存させず、ローカルで実行する。`build` frontend を利用可能にしたうえで次を実行し、wheel / sdist の内容、installed package、CLI、`pip check`、installed wheel を使った dogfood rendering を確認する。

```bash
python scripts/check_dist.py
```

Shikumi の同時リリース準備中など、必要な dependency version がまだ PyPI にない場合は、その source tree を明示して同じ smoke test を行える。

```bash
python scripts/check_dist.py --shikumi-source /path/to/shikumi
```

## Published document

published document は canonical document から利用者ごとの publication workflow で作られる派生物であり、`shikumi-devdoc` はその運用方法を規定しない。翻訳、ローカライズ、文章表現の調整、サイト生成、PDF 化、配布先への配置などはプロジェクトごとに異なり得る。

このリポジトリでは、日本語の canonical document を人間または LLM が英語へ翻訳し、トップレベル `README.md`、`STATUS.md`、`CHANGELOG.md`、`docs/authoring_guide/`、`docs/specification/`、`docs/api/`、およびこの `devdocs/README.md` へ published document として配置する。

`notice.toml` の運用コメントや `shikumi-devdoc:translation-metadata` は published document の内容ではないため、公開時に除去する。

## wheel での配布

`devdocs/` 全体は canonical source と canonical document を対にして読める参照コーパスとして wheel に含める。インストール後は `shikumi_devdoc/resources/devdocs/` に配置される。

同じ wheel には、その版でこのリポジトリが用意した published `README.md`、`STATUS.md`、`CHANGELOG.md`、`docs/` も `shikumi_devdoc/resources/published_docs/` に含める。これはこのリポジトリの配布方針であり、`shikumi-devdoc` が一般に publication workflow を規定することを意味しない。これらは importable public API ではなく package resource である。MIT License 本文は `license-files` による通常の wheel license metadata として配布する。

## sdist での配布

sdist はこの版のリリースソースを再構成・検証するための完全な source distribution とする。実装だけでなく、`tests/`、`devdocs/`、公開 `docs/`、`scripts/`、ルートの公開文書、license、build metadata を含める。`scripts/check_dist.py` 自体も sdist に含め、取得した source distribution から同じ distribution verification を再実行できるようにする。

file selection は個別ファイルを列挙するのではなく、Hatchling が VCS ignore を尊重する既定動作を基礎に、原則としてリリースソース全体を収録する。Git hosting や hosted CI など repository operation にだけ必要な `.github/` は明示的に除外する。cache、virtual environment、`dist/`、IDE metadata など開発機固有または生成済みの一時物は `.gitignore` により配布対象から除外する。
