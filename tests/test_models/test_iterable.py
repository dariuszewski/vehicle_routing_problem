from typing import Any, List
from src.models.iterable import Iterable


import pytest


class ConcreteIterable(Iterable):
    def __init__(self, items: List[Any]):
        super().__init__(items)


def test_base_iterable_iteration():
    items = [1, 2, 3]
    iterable = ConcreteIterable(items)
    for i, item in enumerate(iterable):
        assert item == items[i]


def test_base_iterable_get_item():
    items = [1, 2, 3]
    iterable = ConcreteIterable(items)
    assert iterable[1] == 2


def test_base_iterable_len():
    items = [1, 2, 3]
    iterable = ConcreteIterable(items)
    assert len(iterable) == 3


def test_base_iterable_str():
    items = [1, 2, 3]
    iterable = ConcreteIterable(items)
    assert str(iterable) == str(items)


def test_base_iterable_append():
    items = [1, 2, 3]
    iterable = ConcreteIterable(items)
    iterable.append(4)
    assert iterable[3] == 4
    assert len(iterable) == 4
