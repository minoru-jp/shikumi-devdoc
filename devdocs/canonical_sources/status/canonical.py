"""Canonical Japanese project-status source for shikumi-devdoc."""

from devdocs.canonical_sources.specification.distribution import (
    SPECIFICATION_PART as DISTRIBUTION_SPEC,
)
from shikumi_devdoc.fields.status import GENERAL, condition, kind, related
from devdocs.canonical_sources.vocabulary.canonical import TERMS
from shikumi_devdoc.norms.common import canonical_source, merge
from shikumi_devdoc.norms.document import title


@canonical_source("shikumi-devdoc Project Status", filename="STATUS.md", placeholders=False, heading="identity")
class PROJECT_STATUS:
    r"""
    `shikumi-devdoc` の現在状態と、現在から見た将来の告知を記述する。
    過去の状態変化は保持せず、実際に起きた利用者向け変更は CHANGELOG が担当する。

    この文書は Project Status 専用規定体ではなく、共通 {{TERM_002}} model と `shikumi_devdoc.fields.status` の {{TERM_009}} を組み合わせて記述する。
    """

    merge @= TERMS.TERM_002
    merge @= TERMS.TERM_009

    class STATUS_001:
        r"""現在の開発段階は Beta。現在の公開バージョンは `0.3.1`。"""

        title @= "Development stage"

    class STATUS_002:
        r"""現在の対象 Python バージョン範囲は `>=3.11`。"""

        title @= "Supported Python"

    class STATUS_003:
        r"""`shikumi-devdoc 0.3.1` は `shikumi>=0.2.0` を要求する。互換性の基準線は破壊的変更を行った 0.3.0 で確立した。Shikumi 0.2.0 以降は後方互換性を維持する方針のため、既知の非互換性がない限り上限は設けない。"""

        title @= "Shikumi compatibility"

    class STATUS_004:
        r"""wheel には `devdocs/` 全体と、この版の公開 README、Project Status、CHANGELOG、`docs/` を package resource として含める。"""

        title @= "Installed documentation resources"
        related @= (DISTRIBUTION_SPEC.DIST_001, DISTRIBUTION_SPEC.DIST_002)

    class STATUS_005:
        r"""
        `shikumi-devdoc` は現在 PyPI だけで公開しており、ソースリポジトリを閲覧できる公開 web page はまだ存在しない。そのため README やその他の公開文書にある repository-relative link の一部は、PyPI 上で文書を閲覧した場合には解決しない。これは現在の配布構成で既知の制約である。

        ソースリポジトリを GitHub などで公開した時点で、公開リポジトリ URL を基準として文書 link を見直し、公開文書から正しく解決できるようにする。

        公開ソースリポジトリがまだないため hosted CI も現在は存在しない。release verification と PyPI upload はローカルで行う。GitHub でリポジトリを公開し、その公開環境に対して設定できる時点で CI を導入する。
        """

        title @= "Distribution and CI status"

    class NOTICE_001:
        r"""`0.3.0` の Beta 公開以降、公開 API には破壊的変更を加えず、後方互換性を維持して運用する。実運用とドッグフーディングで API の安定性を確認し、重大な問題がなければメジャーバージョンへ移行する。"""

        title @= "API stability after 0.3.0"
        kind @= GENERAL
        condition @= "`0.3.0` の Beta 公開から最初のメジャーバージョンへ移行するまで。"
