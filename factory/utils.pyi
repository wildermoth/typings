"""
Type stubs for factory.utils module.

Utility functions and classes used throughout factory_boy.
"""

from typing import Any, Callable, Iterable, Sequence, TypeVar, overload
from collections import deque

_T = TypeVar('_T')

def import_object(module_name: str, attribute_name: str) -> Any:
    """
    Import an object from its absolute path.

    Args:
        module_name: The module name (e.g., 'datetime')
        attribute_name: The attribute name (e.g., 'datetime')

    Returns:
        The imported object

    Example:
        >>> import_object('datetime', 'datetime')
        <class 'datetime.datetime'>
    """
    ...

class log_pprint:
    """
    Helper for pretty-printing args/kwargs passed to an object.

    The computation is performed lazily, which is useful when used
    with factory.debug() context manager.
    """
    __slots__ = ['args', 'kwargs']

    args: tuple[Any, ...]
    kwargs: dict[str, Any]

    def __init__(self, args: tuple[Any, ...] = (), kwargs: dict[str, Any] | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...

class ResetableIterator:
    """
    An iterator wrapper that can be reset to its starting point.

    Attributes:
        iterator: The underlying iterator
        past_elements: Deque of elements that have been yielded
        next_elements: Deque of elements to yield next (populated on reset)
    """
    iterator: Iterable[_T]
    past_elements: deque[_T]
    next_elements: deque[_T]

    def __init__(self, iterator: Iterable[_T], **kwargs: Any) -> None: ...
    def __iter__(self) -> Iterable[_T]: ...
    def reset(self) -> None:
        """Reset the iterator to replay all past elements."""
        ...

class OrderedBase:
    """
    Base class for ordered objects.

    Each instance (including subclass instances) shares a global creation counter,
    allowing objects to be sorted by creation order.
    """
    CREATION_COUNTER_FIELD: str  # '_creation_counter'

    def __init__(self, **kwargs: Any) -> None: ...
    def touch_creation_counter(self) -> None:
        """Update this instance's creation counter."""
        ...

@overload
def sort_ordered_objects(items: Iterable[_T]) -> list[_T]: ...

@overload
def sort_ordered_objects(
    items: Iterable[_T],
    getter: Callable[[_T], OrderedBase]
) -> list[_T]: ...

def sort_ordered_objects(
    items: Iterable[_T],
    getter: Callable[[_T], OrderedBase] | None = None
) -> list[_T]:
    """
    Sort an iterable of OrderedBase instances by their creation order.

    Args:
        items: The objects to sort
        getter: Optional function to extract the OrderedBase instance from an object

    Returns:
        Sorted list of items

    Examples:
        >>> sort_ordered_objects([x, y, z])
        >>> sort_ordered_objects(some_dict.items(), getter=lambda e: e[1])
    """
    ...
