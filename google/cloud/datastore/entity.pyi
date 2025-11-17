"""Type stubs for google.cloud.datastore.entity"""

from typing import Any, Dict, Iterable, Optional, Set, Tuple, Union

from google.cloud.datastore.key import Key

class Entity(Dict[str, Any]):
    """Entities are akin to rows in a relational database.

    An Entity is a dictionary-like object that stores property values and
    is uniquely identified by a Key.

    Example:
        entity = Entity(key=key)
        entity['name'] = 'Alice'
        client.put(entity)
    """

    key: Optional[Key]
    exclude_from_indexes: Set[str]
    _meanings: Dict[str, Tuple[Any, Any]]

    def __init__(
        self,
        key: Optional[Key] = ...,
        exclude_from_indexes: Union[Tuple[str, ...], Iterable[str]] = ...
    ) -> None: ...

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...

    @property
    def kind(self) -> Optional[str]:
        """The kind of this entity (from the key)."""
        ...

    @property
    def id(self) -> Optional[int]:
        """The integer ID of this entity (from the key)."""
        ...
