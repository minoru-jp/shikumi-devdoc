"""Shared helpers for canonical-document collections."""

from __future__ import annotations

from types import ModuleType

from shikumi import SemanticView, ViewItem

from shikumi_devdoc.norms._common import CanonicalOrder, CanonicalTitle


def canonical_documents(view: SemanticView) -> list[ViewItem]:
    """Return canonical document roots visible in *view*."""

    return [
        item
        for item in view.entities
        if isinstance(item.node.parent, ModuleType) and item.has(CanonicalTitle)
    ]


def ordered_canonical_documents(view: SemanticView) -> list[ViewItem]:
    """Return canonical document roots in their declared collection order."""

    documents = canonical_documents(view)
    if documents and all(len(item.values(CanonicalOrder)) == 1 for item in documents):
        return sorted(
            documents,
            key=lambda item: (item.values(CanonicalOrder)[0], item.node.path),
        )
    return sorted(documents, key=lambda item: item.node.path)
