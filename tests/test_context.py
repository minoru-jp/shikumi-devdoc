import pytest

from shikumi_devdoc.context import Context, ContextError, UnknownContextKeyError


def test_context_resolves_nested_objects_and_arrays() -> None:
    context = Context({"PROJECT": {"version": "0.1.0"}, "PEOPLE": [{"name": "Minoru"}]})

    assert context.resolve("PROJECT.version") == "0.1.0"
    assert context.resolve("PEOPLE.0.name") == "Minoru"


def test_context_renders_json_non_string_values() -> None:
    context = Context({"BUILD": {"number": 3, "stable": True, "meta": None}})

    assert context.resolve("BUILD.number") == "3"
    assert context.resolve("BUILD.stable") == "true"
    assert context.resolve("BUILD.meta") == "null"


def test_context_from_json_parses_object_string() -> None:
    context = Context.from_json('{"PROJECT":{"name":"Example","version":"0.1.0"}}')

    assert context.resolve("PROJECT.name") == "Example"
    assert context.resolve("PROJECT.version") == "0.1.0"


def test_context_from_json_requires_object_root() -> None:
    with pytest.raises(ContextError):
        Context.from_json("[1,2,3]")


def test_context_from_json_rejects_invalid_json() -> None:
    with pytest.raises(ContextError):
        Context.from_json("{invalid")


def test_unknown_context_key_is_explicit() -> None:
    with pytest.raises(UnknownContextKeyError):
        Context({"PROJECT": {}}).resolve("PROJECT.version")
