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

`shikumi-devdoc` は、**仕様や設計文書を、実装と一緒に育てるためのライブラリ**です。

README、Specification、API Reference、CHANGELOG などの開発文書を、単なる Markdown ファイルではなく、意味と構造を持った Python の **canonical source** として記述します。

文書を「実装が終わったあとに整理するもの」ではなく、開発中も参照・更新される正本として扱いたい場合を想定しています。

## こんな開発に

`shikumi-devdoc` は、特定の開発プロセスそのものを提供するライブラリではありません。

その代わり、仕様や設計を開発の中心に置くための文書基盤を提供します。

たとえば、次のような考え方と組み合わせられます。

- **Spec-Driven Development (SDD)**  
  仕様を実装前の一時的な資料ではなく、実装とともに更新される開発上の正本として扱う。

- **Docs as Code**  
  文書をコードと同じリポジトリで管理し、変更・レビュー・履歴をソフトウェア開発の一部として扱う。

- **LLM-assisted development**  
  LLM に渡す仕様・設計・制約を、散在した文章ではなく、意味と構造を持った開発資産として維持する。

特に SDD では、仕様を書くこと自体よりも、**仕様を実装と乖離させずに維持し続けること**が重要になります。

`shikumi-devdoc` は、その正本を Python 上に置き、人間にも LLM にも扱いやすい文書として維持するための仕組みです。

## このプロジェクト自身がサンプルです

`shikumi-devdoc` 自身の README、Specification、API Reference、CHANGELOG なども `shikumi-devdoc` で管理されています。

実際に使用している canonical source は [`devdocs/canonical_sources/`](https://github.com/minoru-jp/shikumi-devdoc/tree/main/devdocs/canonical_sources) にあります。

ここでは、性格の異なる二つの文書を例にします。

### README: 自由記述を中心とした文書

README のような文書では、大部分は普通の文章です。

canonical source も、その性格をそのまま保って書けます。

````python
from shikumi_devdoc.norms.common import IGNORE, canonical_source
from shikumi_devdoc.norms.document import test_target_field, title


example_source = test_target_field("example source")


@canonical_source(
    "{{project.name}}",
    filename="README.md",
    merge_policy="all",
    unreferenced_fields=IGNORE,
    heading="title",
)
class SECTION_001:
    r"""
    `{{project.name}}` は、仕様や設計文書を
    実装と一緒に育てるためのライブラリです。

    ```python
    {{example_source}}
    ```
    """

    example_source @= r"""
    from shikumi_devdoc.norms.common import canonical_source


    @canonical_source("Example", filename="example.md", merge_policy="local", heading="identity")
    class EXAMPLE:
        class Introduction:
            "Hello from shikumi-devdoc."
    """

    class SECTION_002:
        """このプロジェクト自身の文書も、この仕組みで管理しています。"""

        title @= "このプロジェクト自身がサンプルです"
````

文書の階層は Python の class 構造として表現し、本文は docstring としてそのまま記述できます。

文章主体の文書を、無理に細かなデータ構造へ分解する必要はありません。

必要な部分だけに意味や構造を与えながら、README のような自由な文書をそのまま扱えます。

### Specification: 項目の集合として書く文書

Specification のような文書では、文章そのものよりも、個々の仕様項目が重要になります。

このプロジェクト自身の Specification も、同じ canonical source の仕組みを使っています。

```python
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.fields.specification import MUST, level
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source(
    "Structured fields",
    filename="specification.md",
    order=50,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    class SPEC_001:
        """canonical root 内の class は {{TERM_006}} として解釈されなければならない。"""

        merge @= TERMS.TERM_006
        title @= "Class-derived document-node identity"
        level @= MUST
```

README と Specification は、見た目も使い方もかなり異なります。

一方は自由記述が中心で、もう一方は意味を持つ項目の集合です。

`shikumi-devdoc` では、どちらか一方の形式へ文書を押し込むのではなく、同じ基盤の上でそれぞれの文書に適した形を選べます。

```text
README
  └─ 自由記述が中心
       └─ 必要な情報だけ構造化

Specification
  └─ 項目の集合が中心
       └─ 各項目に意味を持たせる
```

Specification や API Reference は特別な文書 grammar ではありません。

同じ canonical source の上に、その文書で必要な意味を組み合わせて構成されています。

## 値の参照と差し込み

canonical source の template では、固定された文章だけでなく、別に保持した値を `{{name}}` として参照できます。

値の出所は、同じ node に定義した field、別の canonical source から取り込んだ local reference、realization 時に与える external context に分けられます。

### 同じ node に定義した値を参照する

同じ node に `name @= value` として定義した field は、その node の docstring などの template から `{{name}}` で参照できます。

上の README 例にある `example_source` もこの仕組みです。コード例を本文へ直接複製せず、独立した literal text として保持し、表示したい位置から参照しています。

`test_target_field` は、コード、設定、command、期待出力などを**通常のテストから直接参照したいテキストとして分離する**ために使えます。この README の作例コード自体も `test_target_field` として正本ソースから分離され、通常の pytest から対応する example module と構文を比較し、その module を検証・生成しています。

ただし、`test_target_field` に分離しただけで自動的にテストが作られたり実行されたりするわけではありません。何をどのように検証するかは、pytest などプロジェクト側のテスト設計に委ねられます。`test_target_field` はあくまで、テスト可能な単位としてテキストを正本上で独立させるための仕組みです。

### 別の canonical source から差し込む

別の canonical source にある object を、同じ node の local reference として取り込むこともできます。

たとえば、共通の用語を定義して複数の文書から利用する Vocabulary は、この仕組みを使います。

```python
merge @= TERMS.TERM_001
```

用語や定義を文章へ直接複製するのではなく、正本同士の関係として持たせることができます。

Vocabulary は便利な利用例の一つですが、この仕組み自体は Vocabulary 専用ではありません。

### 外部文脈から差し込む

canonical source の外から値を与えることもできます。

たとえば README に表示する現在のバージョン番号や、生成時点で決まる値などです。

```text
canonical source
       +
external context
       ↓
     document
```

このような値を canonical source に直接固定しなくても、文書を生成するときの文脈として与えられます。

## merge policy で差し込み経路を選ぶ

同じ node に直接定義した field は、`merge_policy` にかかわらず template から参照できます。

`merge_policy` が制約するのは、明示的に値を取り込む二つの経路です。

- `merge @= ...` による local merge
- realization 時に与える external context

| policy | `merge @= ...` | external context |
| --- | --- | --- |
| `all` | 利用できる | 利用できる |
| `local` | 利用できる | 利用しない |
| `external` | 利用しない | 利用できる |
| `forbidden` | 利用しない | 利用しない |

この README は external context と local merge の両方を使うため `all`、Specification は local merge だけを使うため `local`、CHANGELOG はどちらも使わないため `forbidden` を指定しています。これは各文書で採用している差し込み方式に合わせた設定であり、文書種別そのものを決定するものではありません。

また、`merge_policy` は Python の値の由来を追跡する仕組みではありません。`name @= value` として同じ node に直接束縛された値は、その評価前にどこで定義されていたかにかかわらず node 自身の field として扱われます。

4種類の厳密な規則は [Authoring Guide](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/authoring_guide/advanced-authoring.md) と [Specification](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/specification/core.md) を参照してください。

## 拡張できます

`shikumi-devdoc` が標準で提供する表現や Markdown 出力は、唯一の使い方ではありません。

基盤には [Shikumi](https://github.com/minoru-jp/shikumi) を使用しています。Shikumi が提供する意味付け・構造化・検証・realization の仕組みについては、[Shikumi documentation](https://github.com/minoru-jp/shikumi/tree/main/docs) を参照してください。

その基盤の上で、`shikumi-devdoc` は二つの方向に拡張できます。

### 独自の意味を表現する

`shikumi-devdoc` が用意している意味表現だけに限定されません。

プロジェクト固有の意味を持つ記述を追加し、同じ canonical source の中で利用できます。

たとえば、独自の開発プロセスで必要になる Requirement、Risk、Decision、Owner、Component、Review status といった情報も表現できます。

既存の文書形式に合わせるのではなく、**そのプロジェクトが必要とする意味を文書へ持たせる**ことができます。

### Markdown 以外へ出力する

`shikumi-devdoc` では Markdown 向けの realizer を提供しています。

別の形式が必要なら、Shikumi の仕組みに沿って独自の realizer を実装できます。

canonical source に持たせた意味と、最終的な出力形式は分離されているため、同じ正本を別の成果物へ展開できます。

## 最小の使い方

PyPI からインストールします。

```bash
pip install shikumi-devdoc
```

最小の canonical source は、root class と nested class だけで記述できます。

```python
from shikumi_devdoc.norms.common import canonical_source


@canonical_source("Example", filename="example.md", merge_policy="local", heading="identity")
class EXAMPLE:
    class Introduction:
        """Hello from shikumi-devdoc."""
```

CLI へ module を渡します。

```bash
shikumi-devdoc render document myproject.example -o build/
```

生成される Markdown は次のようになります。

```markdown
# Example

## Introduction

Hello from shikumi-devdoc.
```

ここから、必要に応じて構造化された情報、差し込み、文書間参照などを追加していけます。

> [!IMPORTANT]
> canonical source は Python module として読み込まれます。信頼できない Python module を文書入力として実行しないでください。

## Documentation

このリポジトリの文書そのものが、`shikumi-devdoc` の実際の利用例です。

- [Authoring Guide](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/authoring_guide/INDEX.md): canonical source を設計・保守するための実践的なガイド。
- [Specification](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/specification/INDEX.md): `shikumi-devdoc` が保証する振る舞いと制約。
- [API Reference](https://github.com/minoru-jp/shikumi-devdoc/blob/main/docs/api/INDEX.md): 公開インターフェース。
- [Project Status](https://github.com/minoru-jp/shikumi-devdoc/blob/main/STATUS.md): 現在の開発状態。
- [CHANGELOG](https://github.com/minoru-jp/shikumi-devdoc/blob/main/CHANGELOG.md): 変更履歴。
- [`devdocs/canonical_sources/`](https://github.com/minoru-jp/shikumi-devdoc/tree/main/devdocs/canonical_sources): このプロジェクト自身が使用している canonical source。
- [`devdocs/canonical_documents/`](https://github.com/minoru-jp/shikumi-devdoc/tree/main/devdocs/canonical_documents): canonical source から生成された日本語 canonical document。
- [devdocs workspace](https://github.com/minoru-jp/shikumi-devdoc/blob/main/devdocs/README.md): このリポジトリにおける canonical document の生成・管理方法。

canonical source と生成された文書を並べて読むことで、`shikumi-devdoc` の実際の運用方法を確認できます。

リポジトリ直下および `docs/` の英語文書は、日本語 canonical document を入力とする別の publication workflow で作成されています。この翻訳・公開工程自体は `shikumi-devdoc` の機能ではありません。

## Version

Current version: `0.3.4`

Supported Python: `>=3.11`

現在の開発段階や互換性に関する情報は [`STATUS.md`](https://github.com/minoru-jp/shikumi-devdoc/blob/main/STATUS.md) を参照してください。

## License

`shikumi-devdoc` is available under the MIT License.

See [`LICENSE`](https://github.com/minoru-jp/shikumi-devdoc/blob/main/LICENSE).
