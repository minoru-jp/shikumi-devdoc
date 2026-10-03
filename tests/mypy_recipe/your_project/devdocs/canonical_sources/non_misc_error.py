"""Negative fixture: non-misc diagnostics must remain visible."""


def expects_text(value: str) -> None:
    del value


expects_text(123)
