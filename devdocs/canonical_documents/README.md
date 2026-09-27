<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/readme/canonical.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を公開工程の入力とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# shikumi-devdoc

`shikumi-devdoc` は、開発文書を意味構造を持つ Python の canonical source として記述し、[Shikumi](https://pypi.org/project/shikumi/) で検証し、Markdown の canonical document へ実現するためのライブラリである。

Vocabulary と共通の canonical document model を二つの基盤として提供する。用語や表記は Vocabulary に集約し、README、Authoring Guide、Project Status、CHANGELOG、Specification、API Reference などは、nested class・docstring template・作者定義 field を組み合わせる同じ document model で構成する。

## 何に使えるのか

`shikumi-devdoc` は、継続的に更新される開発文書について、正本を Python 上の検証可能な意味情報として保ち、必要な realization context を反映して再生成可能な canonical document を得たい場合に使用する。

| 目的 | 基盤 |
| --- | --- |
| 用語の名称と概念定義を一元管理する | Vocabulary |
| README、Authoring Guide、Project Status、CHANGELOG、Specification、API Reference などを構成する | canonical document model |

Specification や API Reference は built-in の文書種別ではない。用途別の意味は作者側の field vocabulary が担い、`shikumi_devdoc.fields` にある standard field set を再利用しても、project-local な field を定義してもよい。

## 最小の使い方

PyPI からインストールする。

```bash
pip install shikumi-devdoc
```

最小の canonical source は `@canonical_source(...)` を付けた root class と、その下に置く nested class だけで記述できる。

```python
from shikumi_devdoc.norms.common import canonical_source

@canonical_source("Example", filename="example.md", placeholders=False, heading="identity")
class EXAMPLE:
    class Introduction:
        '''Hello from shikumi-devdoc.'''
```

module を CLI に渡すと canonical document を生成する。

```bash
shikumi-devdoc render document myproject.example -o build/
```

生成される Markdown は次のようになる。

```markdown
# Example

## Introduction

Hello from shikumi-devdoc.
```

nested class は追加 decorator なしで下位 document node となり、その階層が見出し階層へ対応する。context、field、Vocabulary、index などは必要になった時点で同じモデルへ追加できる。

## コアモデル

`shikumi-devdoc` では Markdown を直接編集して正本とせず、canonical source と realization context から validation と realization を経て canonical document を確定する。

```text
canonical source
      + realization context
        ↓ Shikumi による解釈・検証
     SemanticView
        ↓ shikumi-devdoc の realizer
canonical document
        ↓ project-specific publication workflow
  published document
```

`shikumi-devdoc` が一貫して責任を持つのは canonical document までである。翻訳、ローカライズ、文章表現の調整、媒体変換、配布などは、プロジェクト固有の publication workflow が published document を作る工程として扱う。

canonical document は共通の document node / template / field / merge モデルで記述する。nested class が文書階層、docstring が本文 template、field が構造化された付加情報になる。背景説明のような prose は docstring に保ち、構造として意味を持つ情報だけを field として分離できる。

generic document core は Specification や API Reference の意味論を組み込まない。文書用途を増やすときは別 grammar を増やすのではなく、必要な field vocabulary と presentation を同じ基盤へ組み合わせる。

## Vocabulary と構造化情報

Vocabulary は、用語の名称と概念定義を canonical source として保持する。各 Vocabulary term は `TERM_N` 形式の安定した class identity を持つため、利用文書は実際の用語文字列を複製せず term class を参照できる。

```python
merge @= TERMS.TERM_001
```

template では通常 `{{TERM_001}}` のような短い参照を使える。複数の Vocabulary から同名 identity を取り込んだ場合は、必要な範囲だけ Python identity を修飾して区別できる。具体的な名前解決規則は Specification を参照する。

文書固有の構造化情報は field として宣言する。作者は project-local な field vocabulary を定義でき、頻出する組み合わせには `shikumi_devdoc.fields` の standard field set を利用できる。generic core は field のドメイン意味を所有しない。

docstring、`prose_field`、`title @= ...` は template-bearing content として local reference や external placeholder を扱える。field 系の `@=` 左辺名は同じ node の local reference として自動的に利用でき、`merge` は class target、文字列、明示 alias など追加の参照を登録する。通常の `field`、`list_field`、`table_field`、`test_target_field` の値自体は literal content として扱う。`test_target_field` は通常のテストから直接検証したい文字列断片を分離するためのもので、Markdown fence や language は surrounding template 側に記述する。Python object relation を文書間参照として実現したい場合は `reference_field` を使い、標準 `related` はその convenience field として利用できる。未参照 field は `APPEND` で本文へ追加するか、`IGNORE` で source-only の意味情報として保持できる。

## LLM を介した文書運用

`shikumi-devdoc` は、人間が意図や判断、レビューを担い、LLM が canonical source の継続的な編集を支援する文書運用を主要な利用形態の一つとして想定する。

そのため、記述量の少なさだけを優先せず、意味の明示、機械的な validation、canonical document の安定した再生成を重視する。一方で、LLM の利用は不要な複雑さを許容する理由にはせず、意味の重複や具体的な必要性のない抽象化は避ける。

## Documentation

`shikumi-devdoc` 自身の文書も `shikumi-devdoc` で構築している。

- [Authoring Guide](docs/authoring_guide/INDEX.md): canonical source を設計・保守するための実践的な判断指針。
- [Specification](docs/specification/INDEX.md): 保証する振る舞いと制約。
- [API Reference](docs/api/INDEX.md): 公開インターフェース。
- [Project Status](STATUS.md): 現在状態と現在から見た方向・告知。
- [CHANGELOG](CHANGELOG.md): 過去の変更履歴。
- [devdocs workspace](devdocs/README.md): このリポジトリの文書生成ワークスペース。
- [`devdocs/canonical_sources/`](devdocs/canonical_sources/): 実際に使用している canonical source。
- [`devdocs/canonical_documents/`](devdocs/canonical_documents/): 検証済み source と realization context から生成した日本語 canonical document。

`devdocs/` は authoring API の参照例でもある。canonical source と対応する canonical document を比較すると、記述、context 注入、実現結果の関係を追跡できる。

リポジトリ直下や `docs/` に配置する英語の published document は、日本語 canonical document を入力とする別の publication workflow で作成する。この翻訳・公開工程は `shikumi-devdoc` 自体の機能ではない。

## バージョン

現在のバージョンは `0.3.1`。Python `>=3.11` を対象とする。現在の開発段階や今後の方向は [`STATUS.md`](STATUS.md) を参照する。

## ライセンス

`shikumi-devdoc` は MIT License で提供する。ライセンス本文は [`LICENSE`](LICENSE) を参照すること。
