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


@pytest.mark.parametrize(
    "s",
    ("foo(a, b, 123123)", "foo(a, b, 123.123)"),
    ids=["int", "float"],
)
def test_sim903_true_positive_check(s):
    error_messages = _results(s)
    assert any("SCR903" in error_message for error_message in error_messages)


@pytest.mark.parametrize(
    "s",
    (
        "dict.get('foo', 123)",
        "set_foo(1.23)",
        "line.set_foo(1.23)",
        "partial(foo, 1, 2, 3)",
        "min(0.5, g_norm)",
        "QColor(53, 53, 53, 128)",
    ),
    ids=[
        "get_exception",
        "set_function",
        "set_method",
        "partial",
        "min",
        "color",
    ],
)
def test_sim903_false_positive_check(s):
    error_messages = _results(s)
    for error_message in error_messages:
        assert "SCR903" not in error_message


def test_sim903_insert_exception():
    ret = _results("sys.path.insert(0, 'foo')")
    assert ret == set()


def test_sim903_range_exception():
    ret = _results("range(42)")
    assert ret == set()
