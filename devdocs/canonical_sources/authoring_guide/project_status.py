"""Project-status authoring pattern."""

from devdocs.canonical_sources.api_reference.fields import API_REFERENCE_PART as FIELDS_API
from shikumi_devdoc.fields.common import related
from shikumi_devdoc.norms.common import IGNORE, canonical_source, summary
from shikumi_devdoc.norms.document import title


@summary("現在状態、方向性、利用者向けnoticeを project status document として記述する方法。")
@canonical_source(
    "Writing Project Status",
    filename="project-status.md",
    order=90,
    placeholders=False,
    unreferenced_fields=IGNORE,
    heading="title",
)
class AUTHORING_GUIDE_PART:
    """Project Status は release history ではなく、現在時点の状態と将来方向を説明する。"""

    class SECTION_001:
        r"""
        Beta、experimental、maintenance-only など現在の成熟度、互換性方針、既知の移行予定を README より詳しく伝える必要がある場合に作る。安定状態で特別な告知がない project では不要なことも多い。
        """
        title @= "Project Status を作る場合"

    class SECTION_002:
        r"""
        現在の状態、将来の方向、特定条件での notice を同じ prose に混ぜない。`shikumi_devdoc.fields.status` の `kind`、`condition`、`related` と、`shikumi_devdoc.norms.document.title` は必要な意味だけを構造化するために利用できる。
        """
        title @= "現在事実と将来方向を分ける"

        related @= (FIELDS_API.fields.status,)

    class SECTION_003:
        r"""
        Project Status は現在像を説明し、CHANGELOG は release ごとの過去事実を記録する。状態が変化した場合、現在文書は更新してよいが、過去 release の変更事実は CHANGELOG に残す。
        """
        title @= "CHANGELOG の代わりにしない"
