<!--
この文書は自動生成されています。
正本は `_internal/document_source/readme/canonical.py` です。
直接編集しないでください。

公開文書作成方針

- `_internal/document_build/ja/` にある日本語中間文書を翻訳元とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- `preserve_spelling @= True` が指定された用語は表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは公開文書には含めない。
- 公開文書は翻訳成果物として扱い、内容の変更は公開文書を直接編集するのではなく正本へ戻して行う。
-->

# shikumi-devdoc

`shikumi-devdoc` は、[Shikumi](https://pypi.org/project/shikumi/) を利用して、開発プロジェクトの公開文書を意味情報から記述・検証・実現するための規定体と実現器を提供する Python ライブラリである。

文書、用語、変更履歴を Python 上の正本として記述し、Markdown へ実現できる。プロジェクト名や版など既に別の正本を持つ値は外部から与え、文書ソースへ重複して保持しない。

現在のバージョンは `0.1.0`。Python `>=3.11` を対象とする。

## 目的

`shikumi-devdoc` が扱うのは、完成した Markdown そのものではなく、その手前にある意味構造である。

基本の流れは次のとおり。

```text
Python の記述体
    ↓ Shikumi による解釈・検証
意味像
    ↓ shikumi-devdoc の実現器
日本語 Markdown
    ↓ 必要に応じて翻訳
公開文書
```

正本を Python に置くことで、階層、用語参照、変更区分などを機械的に検証できる。一方、生成された日本語 Markdown は人間が途中結果を読むための中間文書として保持できる。

## 提供する規定体と実現器

初期版では次の三つの文書体系を提供する。

- **文書**: 見出し階層と本文を持つ一般的な開発文書。
- **用語**: 用語名と定義を持つ語彙源。公開対象だけを用語集として実現できる。
- **変更履歴**: リリースと変更項目を持つ構造化された変更履歴。

標準実現器として、それぞれ Markdown への実現を提供する。用語については、人間が IDE 上で `TERM_N` の意味を追跡するための Python 用語参照体 も生成できる。

## インストール

PyPI から導入する場合は次のようにインストールする。

```bash
pip install shikumi-devdoc
```

`shikumi-devdoc` は `shikumi` に依存する。Shikumi 本体は意味の解釈と検証の基盤を担当し、このライブラリは開発文書向けの規定体と実現器をその上に提供する。

## 文書

一般文書は `TITLE_N` クラスの階層として記述する。最外郭には `@canonical` を付け、その記述体が成果物の正本であることを明示する。

```python
from shikumi_devdoc.norms.document import canonical, title


@canonical
@title("Example")
class TITLE_1:
    r'''Project overview.'''

    @title("Install")
    class TITLE_2:
        r'''Installation instructions.'''
```

`@title(...)` の値が見出しになり、クラスの docstring が本文になる。入れ子にした `TITLE_N` は Markdown の見出し階層として実現される。見出し名の変更に影響されない節間リンクが必要な場合は、[安定した見出し参照](#document-anchors)を使用できる。

### 検証と実現

記述体は `document` 規定体で検証し、`DocumentMarkdownRealizer` または `document_markdown.MarkdownRealizer` で Markdown に実現する。

```python
from shikumi_devdoc.norms.document import document
from shikumi_devdoc.realizers import DocumentMarkdownRealizer

result = document.validate(document_source, placement=())
if not result.is_valid:
    raise RuntimeError(result.diagnostics)

realizer = DocumentMarkdownRealizer()
check = realizer.check(result.view)
if not check.is_realizable:
    raise RuntimeError(check.diagnostics)

markdown = realizer.realize(result.view)
```

検証では見出し構造、正本宣言、情報の個数、用語参照の整合性などを確認する。実現前の `check()` では、解決できない 参照記号 など実現上の問題を確認する。本文へ直接書いた Markdown 見出しは意味構造を迂回するため warning とし、7 階層以上の見出しは Markdown で表現できないため error とする。

<a id="document-anchors"></a>

### 安定した見出し参照

見出しを意味的に参照したい場合は、参照先へ `anchor @= "..."` を付ける。Anchor は表示タイトルとは独立しているため、タイトルを変更しても参照先の identity を維持できる。

```python
from shikumi_devdoc.norms.document import anchor, canonical, title


@canonical
@title("Guide")
class TITLE_1:
    r'''See {{#installation}}.'''

    @title("Installation")
    class TITLE_2:
        r'''Installation instructions.'''
        anchor @= "installation"
```

本文中の `{{#installation}}` は `Installation` 見出しへの Markdown link として実現される。参照側に `section_refs` のような別宣言は不要で、`@title` が本文から参照を自動抽出して `SectionReference` として意味像へ保持する。存在しない anchor、同一文書内で重複する anchor、不正な anchor 名は Validator が診断する。

Markdown 実現器は anchor を明示的な HTML `id` として出力するため、見出し文字列から生成されるプラットフォーム固有の slug に依存しない。節参照記法は本文専用で、見出しタイトル中では使用できない。

## 外部情報

プロジェクト名、版、リポジトリ情報など、既に別の正本がある値は文書ソースへ重複して書かず、外部情報 として実現器へ与える。

文書中では 参照記号 を用いて値を参照する。例えば `{{PROJECT.name}}` と `{{PROJECT.version}}` のように、ドット区切りの経路で値を指定する。`\{{...}}` と書いた参照記号は実現時に展開されず、出力ではバックスラッシュを除いた `{{...}}` になる。また `${{...}}` は GitHub Actions など外部構文としてそのまま保持される。

```python
from shikumi_devdoc.realizers import DocumentMarkdownRealizer

realizer = DocumentMarkdownRealizer(
    {
        "PROJECT": {
            "name": "example",
            "version": "0.1.0",
        }
    }
)
```

JSON 文字列から直接構築する場合は `from_json()` を利用できる。

```python
realizer = DocumentMarkdownRealizer.from_json(
    '{"PROJECT":{"name":"example","version":"0.1.0"}}'
)
```

存在しない参照先は黙って空文字へ置換せず、`check()` で診断される。値は文字列だけでなく JSON 互換の配列やオブジェクトも扱える。

## 用語

用語は `VOCABULARY` を最外郭とし、その直下に `TERM_N` を置く。`@term(...)` の値が用語名、docstring が定義になる。

```python
from shikumi_devdoc.norms.vocabulary import (
    alias,
    canonical,
    deprecated,
    glossary,
    preserve_spelling,
    replacement,
    term,
    title,
)


@canonical
@title("Example 用語集")
class VOCABULARY:
    r'''Example で使用する用語。'''

    @term("Widget")
    class TERM_1:
        r'''再利用可能な部品。'''
        glossary @= True
        alias @= "Component"
        alias @= "UI Widget"
```

`glossary @= True` を持つ用語だけが標準の用語集 Markdown 実現器に出力される。内部用の用語は語彙源に残したまま、公開用語集から除外できる。

用語名を翻訳後も同じ表記のまま使用したい場合は、表記維持 を指定する。

```python
@term("Shikumi")
class TERM_2:
    r'''Shikumi の概念を表す名称。'''
    preserve_spelling @= True
```

`preserve_spelling @= True` は「翻訳できない」という意味ではなく、翻訳などによって文書の言語が変わっても、その用語名の表記を変更せず使用するという意味情報である。標準の用語集 Markdown 実現器はこの値を直接使用しない。翻訳用には `TranslationSourceRealizer`、または CLI の `render --translation-source` を使うと、対象用語を機械可読な翻訳メタデータとして中間 Markdown に保持できる。

同じ概念の別名は `alias @= "..."` を複数回記述できる。別名は、同じ Vocabulary 内の canonical な用語名や他の別名と衝突してはならない。用語を廃止予定として残す場合は `deprecated @= True` を付け、推奨する置換先がある場合は `replacement @= "新しい用語名"` で同じ Vocabulary 内の canonical な用語名を指定する。

```python
@term("Widget")
class TERM_1:
    r'''現在使用する用語。'''
    glossary @= True

@term("OldWidget")
class TERM_2:
    r'''旧称。'''
    glossary @= True
    deprecated @= True
    replacement @= "Widget"
```

`replacement` は `deprecated @= True` と組み合わせて使用し、存在しない用語、自分自身、別名を置換先にはできない。標準用語集では別名を表示し、deprecated な公開用語には置換先を含む注意を表示する。

### 用語参照体

正本の語彙では、識別子を `TERM_1`、`TERM_2` のような意味を持たない名前に固定できる。しかし、そのまま文書ソースから参照すると、どの用語なのかを人間が読み取りにくい。

そこで `shikumi-devdoc` は、Vocabulary の意味像から 用語参照体 を生成できる。生成された Python モジュールでは各 `TERM_N` の docstring に用語名と定義が入り、IDE の定義移動やホバー表示から内容を確認できる。

```bash
shikumi-devdoc terms my_project.docs.vocabulary.canonical \
  -o my_project/docs/vocabulary/terms.py
```

出力名や配置場所は利用側が決定する。例えば生成先を `terms.py` とした場合、文書側では次のように利用する。

```python
from my_project.docs.vocabulary import terms
from shikumi_devdoc.norms.document import (
    canonical,
    title,
    vocabulary,
    vocabulary_refs,
)


@canonical
@vocabulary(terms)
@title("API Reference")
class TITLE_1:
    r'''The public API exposes {{TERM_1}}.'''

    vocabulary_refs @= (terms.TERM_1,)
```

`@vocabulary(terms)` は生成モジュールから正本の Vocabulary をたどり、実現時の `TERM_N` 解決に使用する。`vocabulary_refs` に渡した代理クラスも内部では正本の `VOCABULARY.TERM_N` へ戻されるため、意味上の同一性は維持される。

### 用語参照の局所性

`vocabulary_refs` は文書全体へまとめて置かず、その用語を実際に使用する実体へ置く。

```python
@title("Section")
class TITLE_2:
    r'''This section uses {{TERM_1}}.'''

    vocabulary_refs @= (terms.TERM_1,)
```

Validator は各実体について、タイトルと本文に現れる `TERM_N` の集合と、その実体自身の `vocabulary_refs` の集合が完全に一致することを要求する。親から子へ参照は継承されない。同じ `TERM_N` を本文で複数回使用しても、`vocabulary_refs` は一度だけ書けばよい。

この二重記述は意図的である。`TERM_N` の 参照記号 は機械が実現に使い、`vocabulary_refs` は人間が IDE から正規の用語定義へ移動するために使う。Validator が両者の一致を保証する。

## 変更履歴

変更履歴は `CHANGELOG`、`RELEASE_N`、`CHANGE_N` の三階層で記述する。変更区分には `Added`、`Changed`、`Deprecated`、`Removed`、`Fixed`、`Security` を使用できる。

```python
from shikumi_devdoc.norms.changelog import (
    ADDED,
    CHANGED,
    breaking,
    canonical,
    change,
    changelog,
    release,
    released_on,
    unreleased,
)


@canonical
@changelog("Example Changelog")
class CHANGELOG:
    r'''Release history for Example.'''

    @release()
    class RELEASE_1:
        r'''Changes planned for the next release.'''
        unreleased @= True

        @change(CHANGED)
        class CHANGE_1:
            r'''Changed the wire format.'''
            breaking @= True

    @release("0.1.0")
    class RELEASE_2:
        r'''First public release.'''
        released_on @= "2026-09-13"

        @change(ADDED)
        class CHANGE_1:
            r'''Added the initial document system.'''
```

Markdown 実現器はリリースごとに変更項目を区分別にまとめて出力する。文書と同様に `@vocabulary(terms)` と `vocabulary_refs` を使用でき、用語参照は各リリースまたは変更項目の実体単位で検証される。

未公開の変更を保持する場合は、先頭のリリースを `@release()` として `unreleased @= True` を付ける。Unreleased は一つだけ許可され、必ず先頭に置き、`released_on` は指定しない。破壊的変更は個々の `CHANGE_N` に `breaking @= True` を付ける。標準 Markdown 実現器は変更区分を維持したまま、その項目を `Breaking` として明示する。

Changelog は長寿命なプロジェクトで自然に肥大化するため、正本だけを複数モジュールへ物理分割できる。`CHANGELOG` 直下の release は従来どおり先頭の論理 release として扱い、別モジュールの release は `@changelog_part(order=...)` を付けた `CHANGELOG_PART` の直下へ置く。

```python
# released.py
from shikumi_devdoc.norms.changelog import (
    ADDED,
    change,
    changelog_part,
    release,
    released_on,
)


@changelog_part(order=10)
class CHANGELOG_PART:
    @release("1.0.0")
    class RELEASE_1:
        r'''First stable release.'''
        released_on @= "2026-01-01"

        @change(ADDED)
        class CHANGE_1:
            r'''Added the initial feature set.'''
```

package 全体を `changelog_system` または `render changelog` の対象にすると、`CHANGELOG` 直下の release、続いて `order` の昇順の `CHANGELOG_PART`、各 part 内の記述順で一つの論理 Changelog として統合される。ファイル名は順序に影響しない。`order` の重複、release label の重複、複数 part をまたぐ Unreleased の重複も全体で検証される。単一モジュールの従来形式はそのまま利用できる。

## 正本と生成物

文書、用語、変更履歴の最外郭には `@canonical` を付ける。これは場所を推測できる場合でも省略しない。正本であることをソース上で人間が確認できることを優先するためである。

Markdown 実現器は、生成物の先頭へ任意の運用コメントを埋め込める。ただし、注意書きや公開方針の文言は `shikumi-devdoc` 本体では定義しない。文言は利用するプロジェクトの運用側で定義し、実現時に `header_comment` として渡す。

このリポジトリでは `_internal/document_source/notice.toml` に、生成時の注意書きと LLM による公開文書作成方針を、一つの `[notice].content` としてまとめている。`shikumi-devdoc render` に `--notice` でこのファイルを明示的に渡すと、CLI は `{canonical_source}` を対象の正本パスへ置換し、その内容全体を Markdown 実現器の先頭コメントとして渡す。ファイルの自動探索は行わない。

これにより、ライブラリ本体は特定の運用文言を固定せず、各プロジェクトが自分の生成・公開工程に必要な指示を中間文書へ持たせられる。

## 推奨する文書運用

日本語を原文として英語の公開文書を作る場合、次の三層を推奨する。

```text
_internal/document_source/.../canonical.py
    ↓ 実現
_internal/document_build/ja/...md
    ↓ 翻訳
README.md などの公開英語文書
```

`canonical.py` が意味上の正本、日本語 Markdown が人間可読な中間成果物、トップレベルの英語 Markdown が公開成果物となる。

中間文書は Git に含めてよい。これは単なる一時ファイルではなく、規定体が意図どおり実現されたか、翻訳前の日本語が意味的に正しいかを確認する境界面だからである。ただし、中間文書を直接編集してはならない。

公開英語文書への翻訳は機械的なビルド処理ではなく LLM を介した公開工程として扱う。このリポジトリでは、生成時の注意書きと公開時の共通方針を `_internal/document_source/notice.toml` の単一の `notice.content` にまとめる。日本語中間文書を生成するときは、そのファイルを `--notice` で明示的に指定する。

翻訳へ渡す中間文書では `--translation-source` を併用できる。これにより `preserve_spelling @= True` など、通常の Markdown 実現では失われる翻訳向け意味情報が `shikumi-devdoc:translation-metadata` HTML コメントとして埋め込まれる。メタデータ自身は公開文書へ含めない。

そのため、LLM 作業者には日本語中間文書だけを渡せば、翻訳対象の本文、公開時に守るべき方針、表記維持対象を同時に提示できる。

## このリポジトリでのドッグフーディング

`shikumi-devdoc` 自身も同じ仕組みで README と CHANGELOG を生成している。

```text
_internal/
├── document_source/
│   ├── README.md
│   ├── notice.toml
│   ├── readme/
│   │   └── canonical.py
│   ├── changelog/
│   │   ├── canonical.py
│   │   └── released.py
│   └── vocabulary/
│       ├── canonical.py
│       └── terms.py
└── document_build/
    └── ja/
        ├── README.md
        └── CHANGELOG.md
```

`_internal/document_source/README.md` には、このディレクトリに置かれているファイルと、中間文書を生成するときの短い運用手順だけを日本語で記載する。`notice.toml` は運用中にほとんど変化しない共通の注意事項を保持する。

プロジェクト名や版など、その生成時点の値はファイルとして保存せず、必要な値を JSON オブジェクトへまとめたスナップショットとして `--context` に渡す。例えばこの版を生成する場合は次のように実行できる。

```bash
CONTEXT='{"project":{"name":"shikumi-devdoc","version":"0.1.0","requires-python":">=3.11"}}'

shikumi-devdoc terms \
  _internal.document_source.vocabulary.canonical \
  -o _internal/document_source/vocabulary/terms.py

shikumi-devdoc render document \
  _internal.document_source.readme.canonical \
  -o _internal/document_build/ja/README.md \
  --context "$CONTEXT" \
  --notice _internal/document_source/notice.toml \
  --translation-source

shikumi-devdoc render changelog \
  _internal.document_source.changelog \
  -o _internal/document_build/ja/CHANGELOG.md \
  --context "$CONTEXT" \
  --notice _internal/document_source/notice.toml \
  --translation-source
```

`--notice` は固定的な運用文を持つファイルを明示的に指定するための引数であり、CLI は自動探索しない。`--context` はその実現時点の外部情報を表す JSON 文字列を一つ受け取る。どのファイルやシステムからその JSON を組み立てるかは利用側の責務であり、`shikumi-devdoc` はその取得元を知らない。トップレベル `README.md` と `CHANGELOG.md` は、日本語中間文書に埋め込まれた方針に従って LLM で翻訳した公開文書として配置し、公開版には運用コメントを含めない。

## 設計上の境界

`shikumi-devdoc` は汎用テンプレートエンジンを目指さない。

- 条件分岐や繰り返しを含むテンプレート言語は提供しない。
- 参照記号 は用語または 外部情報 の値を明示的に取り込むために使用する。
- 意味構造の検証は Shikumi の規定体として行う。
- Markdown 実現器は意味像を具体的な文書形式へ変換する責務に集中する。
- プロジェクト固有の文書ソースや翻訳工程は利用側に置く。

この境界により、正本、意味情報、実現方法、公開成果物を混ぜずに管理できる。

## ライセンス

`shikumi-devdoc` は MIT License の下で公開する。詳細はトップレベルの `LICENSE` を参照する。
