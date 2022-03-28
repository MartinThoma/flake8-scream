import pytest

from tests import _results


def test_scr119():
    results = _results(
        """
class FooBar:
    def __init__(self, a, b):
        self.a = a
        self.b = b
"""
    )
    assert results == {"2:0 SCR119 Use a dataclass for 'class FooBar'"}


def test_scr119_ignored_dunder_methods():
    """
    Dunder methods do not make a class not be a dataclass candidate.
    Examples for dunder (double underscore) methods are:
      * __str__
      * __eq__
      * __hash__
    """
    results = _results(
        """
class FooBar:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return "FooBar"
"""
    )
    assert results == {"2:0 SCR119 Use a dataclass for 'class FooBar'"}


@pytest.mark.xfail(reason="https://github.com/MartinThoma/flake8-simplify/issues/63")
def test_scr119_false_positive():
    results = _results(
        '''class OfType:
    """
    >>> 3 == OfType(int, str, bool)
    True
    >>> 'txt' == OfType(int)
    False
    """

    def __init__(self, *types):
        self.types = types

    def __eq__(self, other):
        return isinstance(other, self.types)'''
    )
    for el in results:
        assert "SCR119" not in el


def test_scr119_async():
    results = _results(
        """
class FooBar:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    async def foo(self):
        return "FooBar"
"""
    )
    assert results == set()


def test_scr119_constructor_processing():
    results = _results(
        """
class FooBar:
    def __init__(self, a):
        self.a = a + 5
"""
    )
    assert results == set()


def test_scr119_pydantic():
    results = _results(
        """
from pydantic import BaseModel

class FooBar(BaseModel):
    foo : str

    class Config:
        extra = "allow"
"""
    )
    assert results == set()
