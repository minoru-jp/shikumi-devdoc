"""Canonical Japanese project-status source for shikumi-devdoc."""

from devdocs.canonical_sources.specification.distribution import (
    SPECIFICATION_PART as DISTRIBUTION_SPEC,
)
from shikumi_devdoc.fields.status import GENERAL, condition, kind, related
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source("shikumi-devdoc Project Status", filename="STATUS.md", merge_policy="local", heading="identity")
class PROJECT_STATUS:
    r"""
    `shikumi-devdoc` の現在状態と、現在から見た将来の告知を記述する。
    過去の状態変化は保持せず、実際に起きた利用者向け変更は CHANGELOG が担当する。

    この文書は Project Status 専用規定体ではなく、共通 {{TERM_002}} model と `shikumi_devdoc.fields.status` の {{TERM_009}} を組み合わせて記述する。
    """

    merge @= TERMS.TERM_002
    merge @= TERMS.TERM_009

    class STATUS_001:
        r"""現在の開発段階は Beta。現在の公開バージョンは `0.3.3`。"""

        title @= "Development stage"

    class STATUS_002:
        r"""現在の対象 Python バージョン範囲は `>=3.11`。"""

        title @= "Supported Python"

    class STATUS_003:
        r"""`shikumi-devdoc 0.3.3` は `shikumi>=0.2.0` を要求する。互換性の基準線は破壊的変更を行った 0.3.0 で確立した。Shikumi 0.2.0 以降は後方互換性を維持する方針のため、既知の非互換性がない限り上限は設けない。"""

        title @= "Shikumi compatibility"

    class STATUS_004:
        r"""wheel には `devdocs/` 全体と、この版の公開 README、Project Status、CHANGELOG、`docs/` を package resource として含める。"""

        title @= "Installed documentation resources"
        related @= (DISTRIBUTION_SPEC.DIST_001, DISTRIBUTION_SPEC.DIST_002)

    class STATUS_005:
        r"""
        `shikumi-devdoc` は PyPI で配布し、ソースリポジトリを [GitHub](https://github.com/minoru-jp/shikumi-devdoc) で公開している。PyPI に表示される README からも文書へ移動できるよう、README の repository 内参照は公開 GitHub URL を使用する。

        GitHub Actions の CI は `main` への push と pull request で実行し、Python 3.11 から 3.14、最低対応版 `shikumi==0.2.0`、canonical document の同期、test suite、wheel / sdist の build と release distribution verification を確認する。

        GitHub Release を publish すると release workflow が tag と project version の一致を確認し、wheel / sdist を build・検証した後、その検証済み artifact を PyPI Trusted Publishing で公開する。
        """

        title @= "Distribution and CI status"

    class NOTICE_001:
        r"""`0.3.0` の Beta 公開以降、公開 API には破壊的変更を加えず、後方互換性を維持して運用する。実運用とドッグフーディングで API の安定性を確認し、重大な問題がなければメジャーバージョンへ移行する。"""

        title @= "API stability after 0.3.0"
        kind @= GENERAL
        condition @= "`0.3.0` の Beta 公開から最初のメジャーバージョンへ移行するまで。"
    class NOTICE_002:
        r"""`@canonical_source(..., placeholders=...)` は 0.3.2 で非推奨となった。`placeholders=True` は `merge_policy="all"`、`placeholders=False` は `merge_policy="local"` と同じ意味で後方互換に解釈される。新規コードは `merge_policy` を使用する。`placeholders` は 1.0.0 で削除予定である。"""

        title @= "Deprecation of placeholders"
        kind @= GENERAL
        condition @= "`0.3.2` から `1.0.0` へ移行するまで。"

