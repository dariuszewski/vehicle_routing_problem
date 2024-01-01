from typing import Any, List, Iterator
from abc import ABC, abstractmethod


class Iterable(ABC):
    """
    Abstract base class. Provides basic interface for custom iterables.
    """

    def __init__(self, items: List[Any] = []):
        self._items = items

    def __iter__(self) -> Iterator[Any]:
        return iter(self._items)

    def __getitem__(self, index: int) -> Any:
        return self._items[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self._items[index] = value

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return str(self._items)

    def index(self, item) -> Any:
        for i, city in enumerate(self._items):
            if city == item:
                return i
        raise ValueError(f"{item} is not in the route")

    def insert(self, index, item):
        self._items.insert(index, item)

    def remove(self, item):
        self._items.remove(item)

    def append(self, item: Any) -> None:
        self._items.append(item)

    def pop(self):
        self._items.pop()

    def reverse(self):
        self._items.reverse()
