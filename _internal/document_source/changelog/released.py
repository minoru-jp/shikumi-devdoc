"""Released changelog history for shikumi-devdoc."""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.changelog import (
    ADDED,
    CHANGED,
    change,
    changelog_part,
    release,
    released_on,
    vocabulary_refs,
)


@changelog_part(order=10)
class CHANGELOG_PART:
    @release("{{project.version}}")
    class RELEASE_2:
        """最初の公開版。開発文書を Shikumi の意味情報から記述・検証・実現するための基本機能をまとめた。"""

        released_on @= "2026-09-13"

        @change(ADDED)
        class CHANGE_1:
            """一般文書、用語集、変更履歴を記述する規定体と、それぞれを Markdown へ変換する標準実現器を追加した。"""

        @change(ADDED)
        class CHANGE_2:
            """プロジェクト名や版などを {{TERM_1}} として実現器へ渡し、文書中の {{TERM_2}} から参照する仕組みを追加した。"""

            vocabulary_refs @= (
                terms.TERM_1,
                terms.TERM_2,
            )

        @change(ADDED)
        class CHANGE_3:
            """Vocabulary から {{TERM_3}} を生成する CLI を追加し、`TERM_N` から IDE で用語名と定義を追跡できるようにした。"""

            vocabulary_refs @= (terms.TERM_3,)

        @change(ADDED)
        class CHANGE_4:
            """用語参照を使用した実体の近くへ置き、本文中の `TERM_N` と `vocabulary_refs` が実体単位で一致することを Validator で検証する仕組みを追加した。"""

        @change(ADDED)
        class CHANGE_5:
            """正本を `@canonical` で明示し、Markdown 実現器へ運用側から任意の先頭コメントを渡せる仕組みを追加した。"""

        @change(CHANGED)
        class CHANGE_6:
            """用語の翻訳方針を表す情報名を `untranslatable` から `preserve_spelling` へ変更し、「翻訳不能」ではなく {{TERM_4}} を意味することを明確にした。"""

            vocabulary_refs @= (terms.TERM_4,)

        @change(ADDED)
        class CHANGE_7:
            """正本の Python 記述体から日本語の中間文書を生成し、その英訳をリポジトリ直下の公開文書として配置するドッグフーディング運用を追加した。"""

        @change(CHANGED)
        class CHANGE_8:
            """生成時の注意書きと LLM による公開文書作成方針を運用側の `notice.toml` の単一の `notice.content` にまとめた。`render --notice` で明示的に指定した場合だけ中間文書へ埋め込み、設定ファイルの自動探索は行わない。あわせてリポジトリ固有の `build_docs.py` を廃止し、用語参照体生成と中間文書生成を CLI から直接実行する形へ整理した。"""

        @change(CHANGED)
        class CHANGE_9:
            """`render --context` を外部情報ファイルの指定ではなく、実現時点のスナップショットを表す単一の JSON 文字列として受け取る形へ整理した。`notice.toml` は固定的な運用文、`--context` は可変な値という役割を分離し、`_internal/document_source/README.md` にこのリポジトリでの生成手順を記載した。"""

        @change(CHANGED)
        class CHANGE_10:
            r"""Placeholder の字句処理を共通化し、`\\{{...}}` による literal escape と `${{...}}` の保持を追加した。用語参照検証も同じ字句規則を使用するため、escape された marker を意味参照として誤認しない。"""

        @change(ADDED)
        class CHANGE_11:
            """翻訳用中間 Markdown に `preserve_spelling` 対象を機械可読なメタデータとして保持する `TranslationSourceRealizer` と `render --translation-source` を追加した。"""

        @change(CHANGED)
        class CHANGE_12:
            """CLI diagnostics に severity、diagnostic code、Python source location、semantic subject を表示するよう改善し、本文中の raw Markdown heading と Markdown の6階層制限を実現前に検査するようにした。"""

        @change(ADDED)
        class CHANGE_13:
            r"""文書見出しへ `anchor @= "..."` で安定した identity を付与し、本文中の `\{{#anchor}}` から意味的に節を参照する仕組みを追加した。参照は `SectionReference` として意味像へ自動抽出され、未知参照、anchor の重複、不正な anchor 名を検証する。"""

