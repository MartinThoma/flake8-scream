from tests import _results


def test_scr204_base():
    ret = _results("not a < b")
    assert ret == {("1:0 SCR204 Use 'a >= b' instead of 'not (a < b)'")}


def test_scr205_base():
    ret = _results("not a <= b")
    assert ret == {("1:0 SCR205 Use 'a > b' instead of 'not (a <= b)'")}


def test_scr206_base():
    ret = _results("not a > b")
    assert ret == {("1:0 SCR206 Use 'a <= b' instead of 'not (a > b)'")}


def test_scr207_base():
    ret = _results("not a >= b")
    assert ret == {("1:0 SCR207 Use 'a < b' instead of 'not (a >= b)'")}
