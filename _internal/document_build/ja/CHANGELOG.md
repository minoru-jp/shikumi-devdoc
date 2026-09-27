<!--
この文書は自動生成されています。
正本は `_internal/document_source/changelog/canonical.py` です。
直接編集しないでください。

公開文書作成方針

- `_internal/document_build/ja/` にある日本語中間文書を翻訳元とする。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- `preserve_spelling @= True` が指定された用語は表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックは公開文書には含めない。
- 公開文書は翻訳成果物として扱い、内容の変更は公開文書を直接編集するのではなく正本へ戻して行う。
-->

# shikumi-devdoc 変更履歴

`shikumi-devdoc` の公開版に含まれる変更を記録する。

## Unreleased

次の公開版へ向けた未公開の変更。

### Added

- Vocabulary に複数の `alias`、`deprecated`、`replacement` を追加し、公開用語の別名と廃止・置換関係を意味情報として検証・実現できるようにした。
- Changelog に `unreleased` と `breaking` を追加した。Unreleased は一つだけ先頭に置き日付を持たず、breaking な変更項目は元の変更区分を維持したまま Markdown 上で明示される。
- Changelog の正本を複数モジュールへ物理分割し、`@changelog_part(order=...)` で論理的な一つの変更履歴として統合・検証・実現できるようにした。

## 0.1.0 - 2026-09-13

最初の公開版。開発文書を Shikumi の意味情報から記述・検証・実現するための基本機能をまとめた。

### Added

- 一般文書、用語集、変更履歴を記述する規定体と、それぞれを Markdown へ変換する標準実現器を追加した。
- プロジェクト名や版などを 外部情報 として実現器へ渡し、文書中の 参照記号 から参照する仕組みを追加した。
- Vocabulary から 用語参照体 を生成する CLI を追加し、`TERM_N` から IDE で用語名と定義を追跡できるようにした。
- 用語参照を使用した実体の近くへ置き、本文中の `TERM_N` と `vocabulary_refs` が実体単位で一致することを Validator で検証する仕組みを追加した。
- 正本を `@canonical` で明示し、Markdown 実現器へ運用側から任意の先頭コメントを渡せる仕組みを追加した。
- 正本の Python 記述体から日本語の中間文書を生成し、その英訳をリポジトリ直下の公開文書として配置するドッグフーディング運用を追加した。
- 翻訳用中間 Markdown に `preserve_spelling` 対象を機械可読なメタデータとして保持する `TranslationSourceRealizer` と `render --translation-source` を追加した。
- 文書見出しへ `anchor @= "..."` で安定した identity を付与し、本文中の `{{#anchor}}` から意味的に節を参照する仕組みを追加した。参照は `SectionReference` として意味像へ自動抽出され、未知参照、anchor の重複、不正な anchor 名を検証する。

### Changed

- 用語の翻訳方針を表す情報名を `untranslatable` から `preserve_spelling` へ変更し、「翻訳不能」ではなく 表記維持 を意味することを明確にした。
- 生成時の注意書きと LLM による公開文書作成方針を運用側の `notice.toml` の単一の `notice.content` にまとめた。`render --notice` で明示的に指定した場合だけ中間文書へ埋め込み、設定ファイルの自動探索は行わない。あわせてリポジトリ固有の `build_docs.py` を廃止し、用語参照体生成と中間文書生成を CLI から直接実行する形へ整理した。
- `render --context` を外部情報ファイルの指定ではなく、実現時点のスナップショットを表す単一の JSON 文字列として受け取る形へ整理した。`notice.toml` は固定的な運用文、`--context` は可変な値という役割を分離し、`_internal/document_source/README.md` にこのリポジトリでの生成手順を記載した。
- Placeholder の字句処理を共通化し、`\{{...}}` による literal escape と `${{...}}` の保持を追加した。用語参照検証も同じ字句規則を使用するため、escape された marker を意味参照として誤認しない。
- CLI diagnostics に severity、diagnostic code、Python source location、semantic subject を表示するよう改善し、本文中の raw Markdown heading と Markdown の6階層制限を実現前に検査するようにした。
