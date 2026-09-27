"""External JSON-compatible context used by document realizers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import json
from typing import Any


class ContextError(ValueError):
    """Base error for invalid or unresolved realization context."""


class UnknownContextKeyError(ContextError):
    """Raised when a placeholder path cannot be resolved."""

    def __init__(self, key: str) -> None:
        super().__init__(f"unknown context key: {key}")
        self.key = key


@dataclass(frozen=True, slots=True)
class Context:
    """A JSON-compatible mapping addressable through dotted paths.

    ``PROJECT.version`` resolves ``{"PROJECT": {"version": ...}}``.
    Numeric path components can index arrays, e.g. ``PEOPLE.0.name``.
    """

    data: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.data, Mapping):
            raise TypeError("context root must be a mapping")

    @classmethod
    def from_json(cls, text: str) -> "Context":
        """Create context from a JSON object string."""
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ContextError(f"invalid context JSON: {exc.msg}") from exc
        if not isinstance(data, dict):
            raise ContextError("context JSON root must be an object")
        return cls(data)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "Context":
        return cls(data)

    def resolve(self, key: str) -> str:
        if not isinstance(key, str) or not key or any(not part for part in key.split(".")):
            raise UnknownContextKeyError(key)

        value: Any = self.data
        for part in key.split("."):
            if isinstance(value, Mapping):
                if part not in value:
                    raise UnknownContextKeyError(key)
                value = value[part]
                continue
            if (
                isinstance(value, Sequence)
                and not isinstance(value, (str, bytes, bytearray))
                and part.isdecimal()
            ):
                index = int(part)
                if index >= len(value):
                    raise UnknownContextKeyError(key)
                value = value[index]
                continue
            raise UnknownContextKeyError(key)

        if isinstance(value, str):
            return value
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

    def contains(self, key: str) -> bool:
        try:
            self.resolve(key)
        except UnknownContextKeyError:
            return False
        return True


EMPTY_CONTEXT = Context({})


def normalize_context(value: Context | Mapping[str, Any] | None) -> Context:
    if value is None:
        return EMPTY_CONTEXT
    if isinstance(value, Context):
        return value
    if isinstance(value, Mapping):
        return Context(value)
    raise TypeError("context must be a Context, mapping, or None")
