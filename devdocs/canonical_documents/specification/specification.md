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

# Structured fields

作者定義 field と自己完結した canonical document に関する規則。

## SPEC_001

canonical root の内部で字句的に定義された class は document node として解釈され、その identity は Python クラス名と class の入れ子から導出されなければならない。個々の node に専用 decorator を要求してはならない。

title: Class-derived document-node identity

level: MUST

## SPEC_002

`field(name, value_type, ...)` などが宣言する canonical display name と Python 上で writer を保持する変数名、および `@=` を記述する左辺 binding name は独立でなければならない。

title: Author-defined field names

level: MUST

## SPEC_003

各 canonical document は `@canonical_source(..., filename=...)` に自身が生成する Markdown の filename を明示し、それ単独で検証・実現可能でなければならない。

title: Self-contained document filename

level: MUST

## SPEC_004

`@canonical_source(..., order=...)` は複数文書を安定順で扱いたい場合だけ指定してよい。

title: Optional document order

level: MAY

## SPEC_005

document node の入れ子は canonical Markdown の見出し入れ子そのものとして解釈しなければならない。Markdown で表現できない深度は realization check で拒否する。

title: Node nesting is heading nesting

level: MUST

condition: Markdown へ実現する場合。

## SPEC_006

未参照 field を自動実現する場合でも、field name だけを根拠に Markdown heading へ昇格させてはならない。field presentation は field factory が宣言する文書構造に従う。

title: Fields are not headings

level: MUST

## SPEC_007

Specification、API Reference、ADR などのドメイン field vocabulary は `field()` などの writer の組として利用側または別ライブラリで定義できなければならない。

title: External domain field vocabularies

level: MUST

## SPEC_008

field value として Python class を使用する場合、その実体は評価時点で解決済みでなければならない。基盤は文字列 ID、forward reference、symbolic reference の解決機構を追加しない。

title: Direct Python references

level: MUST

## SPEC_009

個別 canonical document の実現と collection index の実現は独立した操作でなければならない。標準 document realizer は `INDEX.md` を暗黙生成せず、index realizer は明示的に指定された package の canonical source 集合から索引だけを生成する。

title: Separate document and index realization

level: MUST

## SPEC_010

realizer は document node hierarchy をドメイン意味から再編集せず、作者が記述した class hierarchy をそのまま Markdown heading hierarchy へ写像しなければならない。

title: Preserve author hierarchy

level: MUST

## SPEC_011

複数の canonical document は共通 root entity への依存を持たず、それぞれ独立した `@canonical_source(...)` root の集合として扱われなければならない。

title: No collection-root dependency

level: MUST
