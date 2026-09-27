"""Canonical Japanese changelog source for shikumi-devdoc."""

from _internal.document_source.vocabulary import terms
from shikumi_devdoc.norms.changelog import (
    ADDED,
    canonical,
    change,
    changelog,
    release,
    unreleased,
    vocabulary,
)


@canonical
@vocabulary(terms)
@changelog("{{project.name}} 変更履歴")
class CHANGELOG:
    """`{{project.name}}` の公開版に含まれる変更を記録する。"""

    @release()
    class RELEASE_1:
        """次の公開版へ向けた未公開の変更。"""

        unreleased @= True

        @change(ADDED)
        class CHANGE_1:
            """Vocabulary に複数の `alias`、`deprecated`、`replacement` を追加し、公開用語の別名と廃止・置換関係を意味情報として検証・実現できるようにした。"""

        @change(ADDED)
        class CHANGE_2:
            """Changelog に `unreleased` と `breaking` を追加した。Unreleased は一つだけ先頭に置き日付を持たず、breaking な変更項目は元の変更区分を維持したまま Markdown 上で明示される。"""

        @change(ADDED)
        class CHANGE_3:
            """Changelog の正本を複数モジュールへ物理分割し、`@changelog_part(order=...)` で論理的な一つの変更履歴として統合・検証・実現できるようにした。"""

