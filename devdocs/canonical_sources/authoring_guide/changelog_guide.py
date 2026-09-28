"""CHANGELOG authoring pattern."""

from devdocs.canonical_sources.api_reference.fields import API_REFERENCE_PART as FIELDS_API
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import test_target_field, title


changelog_example = test_target_field("CHANGELOG example")
lifecycle_example = test_target_field("lifecycle example")


@summary("release 単位の変更履歴を changelog field set で記録し、subject lifecycle と分離する方法。")
@canonical_source(
    "Writing a CHANGELOG",
    filename="changelog.md",
    order=70,
    merge_policy="local",
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """CHANGELOG は release-centered な歴史記録として、後から意味が変わらない事実を canonical source に保持する。"""

    class SECTION_001:
        r"""
        利用者が release ごとの差分、breaking change、修正内容を追う必要がある場合に作る。内部開発メモだけで十分な project では必須ではない。
        """
        title @= "CHANGELOG を作る場合"

    class SECTION_002:
        r"""
        release ごとに node を作り、`shikumi_devdoc.fields.changelog` の `version`、`released_on`、`added`、`changed`、`deprecated`、`removed`、`fixed`、`security` から必要な field を使う。

        ```python
        {{changelog_example}}
        ```

        change-category field は literal list content である。`\{{...}}` を展開する template として扱わず、歴史記録として残したい文言をそのまま書く。
        """
        title @= "Release を node にする"

        changelog_example @= r'''
        from shikumi_devdoc.fields.changelog import added, fixed, version

        class V1_2_0:
            """Release 1.2.0."""

            version @= "1.2.0"
            added @= "Added the public `run()` operation."
            fixed @= "Fixed configuration-path resolution."
        '''
        related @= (FIELDS_API.fields.changelog,)

    class SECTION_003:
        r"""
        現在の project version は realization context に置けるが、過去 release の version や変更内容は canonical source に固定する。再実現したときに過去の CHANGELOG が現在値へ書き換わる設計にしない。CHANGELOG 自体の `@canonical_source(...)` には `merge_policy="forbidden"` を指定し、local merge と external merge の双方を拒否する。
        """
        title @= "Current context と歴史的事実を分ける"

    class SECTION_004:
        r"""
        API や設定項目の導入・非推奨・削除を、その対象を読む利用者からも確認させたい場合は lifecycle field を対象自身へ付ける。

        ```python
        {{lifecycle_example}}
        ```
        """
        title @= "Subject lifecycle は対象文書にも残せる"

        lifecycle_example @= r'''
        introduced @= "0.2.0"
        deprecated @= "0.4.0"
        replacement @= "new_api"
        migration @= "Replace `old_api` with `new_api` when updating callers."
        '''
        related @= (FIELDS_API.fields.lifecycle,)
