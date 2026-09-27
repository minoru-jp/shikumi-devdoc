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

# Writing a Glossary / Vocabulary

Vocabulary は複数文書で正式名称と概念定義を共有する必要がある場合だけ導入する。

## Glossary / Vocabulary を作る場合

project 固有の用語が複数文書で繰り返され、名称変更や定義を一か所で管理したい場合に Vocabulary を作る。一般語や一度しか使わない語まで Vocabulary 化しない。

Vocabulary term は既定で Glossary の公開対象になる。内部用 term など公開したくないものだけ `glossary @= False` を明示する。`glossary @= True` は既定値と同じなので通常は書かない。

## Stable term identity を定義する

term class は `TERM_NNN` のような stable identity を持たせ、正規化された docstring の先頭へ `{{term name}}` declaration を一つだけ書く。docstring は通常の Python indentation に合わせてよい。

```python
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.vocabulary import vocabulary


@vocabulary
@canonical_source("Project Vocabulary", filename="GLOSSARY.md", placeholders=False, heading="identity")
class TERMS:
    class TERM_001:
        """
        {{project term}}

        プロジェクト内で共有する概念の簡潔な定義。
        """
```

## 利用する node で直接 merge する

文書全体へ暗黙に Vocabulary を接続せず、その term を使う document node で canonical term class を直接 `merge` する。

```python
class Overview:
    """この文書の正本は {{TERM_001}} である。"""

    merge @= TERMS.TERM_001
```

## 外部 Vocabulary も同じように参照する

別 package の Vocabulary でも、import した term class を直接 merge target にする。

```python
merge @= FrameworkVocabulary.TERM_001
```

同じ短い `TERM_001` が衝突した場合だけ、より長い Python identity や明示 alias で区別する。最初から完全修飾名を多用しない。
