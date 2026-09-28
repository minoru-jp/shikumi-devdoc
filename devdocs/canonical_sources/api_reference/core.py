"""Core API reference part."""
from shikumi_devdoc.fields.api_reference import detail, input, kind, name, output, related, NAMESPACE, TYPE, VALUE, OPERATION, OTHER, API_NAMESPACE, API_TYPE, API_VALUE, API_OPERATION, API_OTHER
from shikumi_devdoc.norms.common import canonical_source, summary
from devdocs.canonical_sources.specification.distribution import SPECIFICATION_PART as DISTRIBUTION_SPEC

@summary('トップレベルの公開名前空間と主要エントリポイント。')
@canonical_source('Core', filename='core.md', order=0, merge_policy="all", heading="identity")
class API_REFERENCE_PART:
    """トップレベルの公開名前空間。"""

    class shikumi_devdoc:
        """小さな入口名前空間。Context 系と、標準 field、authoring、realization の名前空間を公開する。"""
        name @= 'shikumi_devdoc'
        kind @= NAMESPACE
        related @= (DISTRIBUTION_SPEC.DIST_006,)
        detail @= 'Exports: `Context`、`ContextError`、`UnknownContextKeyError`、`fields`、`norms`、`realizers` を公開する。`fields`、`norms`、`realizers` はさらに用途・意味領域ごとの中分類 namespace を公開する。'
