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

# Field presentations

作者定義 field が canonical Markdown 上で選択できる汎用表現に関する規則。

## FIELD_001

field factory は authoring intent を名前として表してよいが、generic realizer の挙動は factory が明示した literal/template/reference と文書構造上の契約だけに従わなければならない。field 名や値から追加のドメイン意味や presentation を推論してはならない。

title: Explicit field behavior

level: MUST

## FIELD_002

`field()` は単一または反復する literal 値を compact な inline content として保持し、未参照 field を APPEND する場合は `name: value` を基本形として実現しなければならない。

title: Inline field

level: MUST

## FIELD_003

`list_field()` は各 `@=` 値を同じ field の Markdown bullet list item として実現しなければならない。

title: List field

level: MUST

## FIELD_004

`test_target_field()` は通常のテストから独立して参照・検証したい文字列断片を literal test target として保持しなければならない。Realizer はその値へ fenced code block、language info string、その他の Markdown presentation を暗黙に付加してはならず、template へ参照された位置に正規化済み literal text だけを挿入しなければならない。

title: Test target field

level: MUST

## FIELD_005

`test_target_field()` は作者が通常のテストから直接参照したい断片であることを示すが、その断片に対応するテストが存在すること、またはテストに合格していることを自動保証してはならない。

title: Test coverage is not implied

level: MUST NOT

## FIELD_006

`test_target_field()` の値をコード、設定、command、expected output などとして文書化する場合、Markdown fence や言語指定などの presentation は docstring または `prose_field` template 側へ記述し、対応する通常のテストから field 値そのものを検証することが望ましい。

title: Test-target presentation and verification

level: SHOULD

## FIELD_007

`table_field()` は宣言された column と同じ幅を持つ各 `@=` row を Markdown table の一行として実現し、row 幅の不一致を validation error としなければならない。

title: Table field

level: MUST

## FIELD_008

`prose_field()` は名前付きの Markdown prose template fragment を保持し、docstring template と同じ local reference、external placeholder、escape 規則で実現しなければならない。

title: Prose field

level: MUST

## FIELD_009

literal field と `prose_field` の区別は値のドメイン意味ではなく、値を template-bearing content として解釈するか literal content として保持するかを決定する presentation 契約でなければならない。

title: Template-bearing versus literal fields

level: MUST

## FIELD_010

`reference_field()` は Python object relation を literal text へ平坦化せず semantic reference として保持しなければならない。Markdown realizer は参照元と参照対象の canonical document logical path、および参照対象の rendered heading を解決できる場合、それらから決定論的な relative logical Markdown link を実現し、解決できない値は literal field と同等の安定した表現へ fallback しなければならない。

title: Reference field

level: MUST
