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

# Writing a README

README は repository の入口として、採用判断と次の行動に必要な情報へ集中させる。

## README を作る場合

repository を初めて見る読者へ、何をする project か、どう導入するか、最初に何を実行するか、詳細をどこで読むかを示したい場合に README を作る。内部仕様、全設定項目、全 API を README へ詰め込む必要はない。

README だけで十分な project なら、他の authoring pattern を形式的に追加しない。

## 推奨構造

多くの場合、次の順序で十分である。

1. project が何をするかを短く説明する。
2. 重要な利用条件や安全上の境界があれば早い位置に置く。
3. installation を示す。
4. 最小の利用例を示す。
5. CLI、Configuration、API Reference、Specification など、実際に存在する詳細文書へリンクする。

長い tutorial や完全な reference が必要になったら README を伸ばし続けず、Getting Started や専用 guide へ分ける。

## 正本は prose 中心でよい

README は narrative document なので、通常は docstring prose と nested document node を中心に構成する。見出し構造は nested class と `title @= ...` で表し、表示 title と class identity は分離する。root の `heading="title"` が title を見出しへ実現する。

コード例を通常のテストから直接検証して実装 drift を防ぎたい場合だけ `test_target_field` に分離する。小さな例示コードは docstring に直接書いてよい。fence は docstring 側に置き、現在 version のように再実現時に変わってよい値だけを realization context に置く。

## 最小例

```python
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source(
    "Example", filename="README.md", merge_policy="local", heading="title"
)
class README:
    """A small tool for processing example inputs."""

    class SECTION_001:
        """Install the package with your normal Python package workflow."""

        title @= "Installation"

    class SECTION_002:
        """Run the smallest useful example, then link to detailed guides."""

        title @= "Quick start"
```

README 固有の schema はない。これは generic canonical document の一例であり、必要な節だけを追加する。

## 避けること

README に全 CLI option、全設定 schema、全 normative rule を重複して書かない。README は概要と導線を担い、詳細の正本はそれぞれの目的文書へ置く。

README の見出し名を class name に反映し続ける必要もない。タイトル変更で identity が drift する場合は `SECTION_NNN` のような opaque identity を使う。
