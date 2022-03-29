import pytest

from tests import _results


@pytest.mark.parametrize(
    "s",
    (
        "foo(a, b, True)",
        "set_foo(a, b, True)",
    ),
    ids=[
        "basic",
        "set_multiple",
    ],
)
def test_scr902(s):
    error_messages = _results(s)
    assert any("SCR902" in error_message for error_message in error_messages)


@pytest.mark.parametrize(
    "s",
    (
        "foo(a, b, foo=True)",
        "dict.get('foo', True)",
        "set_visible(True)",
        "line.set_visible(True)",
        "partial(foo, True)",
        "partial(foo, bar=True)",
        "getattr(foo, 'bar', True)",
    ),
    ids=[
        "kw_arg_is_used",
        "dict_get",
        "boolean_setter_function",
        "boolean_setter_method",
        "partial_arg",
        "partial_kwarg",
        "getattr",
    ],
)
def test_scr902_false_positive_check(s):
    error_messages = _results(s)
    for error_message in error_messages:
        assert "SCR902" not in error_message
