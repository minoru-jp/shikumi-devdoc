"""Document-collection authoring pattern."""

from devdocs.canonical_sources.specification.specification import (
    SPECIFICATION_PART as STRUCTURED_SPEC,
)
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import test_target_field, title

collection_example = test_target_field("collection layout")


@summary(
    "大きな文書を意味領域ごとの独立 canonical document に分け、INDEX を別 realization する方法。"
)
@canonical_source(
    "Building a document collection",
    filename="collections.md",
    order=100,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """Collection は、独立して読めて独立して変更できる canonical document の集合として構成する。"""

    class SECTION_001:
        r"""
        一つの文書が長いという理由だけではなく、意味領域ごとに変更責務、参照先、読者の目的が独立してきた場合に collection 化する。Specification、API Reference、Configuration Guide、CLI documentation などは collection に育ちやすい。

        小さい文書を形式的に分割しない。読者が全ページを順番に読まなければ意味が成立しない場合は、一枚の document の方が自然なこともある。
        """

        title @= "Collection を作る場合"

    class SECTION_002:
        r"""
        collection 全体の専用 grammar を作るのではなく、各ページをそれぞれ `@canonical_source(...)` root とする。各 document は単独で validation / realization できる状態を保つ。

        ```text
        {{collection_example}}
        ```
        """

        title @= "各 document を独立した canonical source にする"

        collection_example @= r"""
        canonical_sources/
          specification/
            __init__.py
            overview.py
            paths.py
            output.py
        """
        related @= (STRUCTURED_SPEC.SPEC_003, STRUCTURED_SPEC.SPEC_011)

    class SECTION_003:
        r"""
        人間向けに安定順が必要なら `@canonical_source(..., order=...)` を指定し、INDEX で各文書の役割を示したい場合は `@summary(...)` を付ける。order は文書内容の identity ではなく collection presentation のための metadata として扱う。
        """

        title @= "順序と summary を metadata にする"

    class SECTION_004:
        r"""
        individual document と collection index の生成を分ける。document realizer に暗黙の `INDEX.md` 生成を持たせず、`render index` / `IndexMarkdownRealizer` で collection package から index を生成する。

        公開工程で翻訳する場合も、INDEX だけに canonical source にない説明を追加せず、各 document の `@summary(...)` に戻して正本を更新する。
        """

        title @= "INDEX は別 realization にする"

        related @= (STRUCTURED_SPEC.SPEC_009,)
