"""Shared validation helpers for partitioned devdoc regulations."""

from __future__ import annotations

from pathlib import PurePosixPath, PureWindowsPath


def filename_value_error(filename: object, *, label: str = "filename") -> str | None:
    """Return a user-facing validation error for a declared output filename."""

    if not isinstance(filename, str):
        return f"{label} must be a string"
    if not filename.strip() or filename in {".", ".."}:
        return f"{label} must be a non-empty file name"
    if "\x00" in filename:
        return f"{label} must not contain NUL"
    if (
        PurePosixPath(filename).name != filename
        or PureWindowsPath(filename).name != filename
    ):
        return f"{label} must not contain a directory path"
    return None


def validate_filename(filename: object, *, label: str = "filename") -> str:
    """Validate one declarative output filename at description time."""

    error = filename_value_error(filename, label=label)
    if error is None and isinstance(filename, str):
        return filename
    if not isinstance(filename, str):
        raise TypeError(error)
    raise ValueError(error)


def validate_optional_order(
    order: int | None, *, label: str = "part order"
) -> int | None:
    """Validate an optional non-negative integer order at description time."""

    if order is None:
        return None
    if isinstance(order, bool) or not isinstance(order, int):
        raise TypeError(f"{label} must be an integer or None")
    if order < 0:
        raise ValueError(f"{label} must be non-negative")
    return order
