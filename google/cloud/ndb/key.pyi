"""Type stubs for google.cloud.ndb.key"""

from typing import Any, Dict, Iterable, List, Optional, Tuple, Union, overload

UNDEFINED: object

class Key:
    """An immutable datastore key.

    A Key uniquely identifies a datastore entity. Keys can be constructed in
    several ways:
    - Using positional args: Key('Kind', id_or_name, 'Kind2', id_or_name2, ...)
    - Using pairs: Key(pairs=[('Kind', id_or_name), ...])
    - Using flat: Key(flat=['Kind', id_or_name, ...])
    - From urlsafe: Key(urlsafe=b'...')
    """

    def __init__(
        self,
        *args: Union[str, int, type],
        pairs: Optional[List[Tuple[str, Union[str, int, None]]]] = ...,
        flat: Optional[List[Union[str, int]]] = ...,
        parent: Optional[Key] = ...,
        namespace: Optional[str] = ...,
        app: Optional[str] = ...,
        project: Optional[str] = ...,
        database: Optional[str] = ...,
        urlsafe: Optional[Union[str, bytes]] = ...,
        reference: Optional[Any] = ...,
        serialized: Optional[bytes] = ...,
    ) -> None: ...

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self) -> str: ...
    def __lt__(self, other: Key) -> bool: ...
    def __le__(self, other: Key) -> bool: ...
    def __gt__(self, other: Key) -> bool: ...
    def __ge__(self, other: Key) -> bool: ...

    @overload
    def __getstate__(self) -> Tuple[bytes]: ...
    @overload
    def __setstate__(self, state: Tuple[bytes]) -> None: ...

    def app(self) -> str:
        """Return the application ID (project ID) for this key."""
        ...

    def pairs(self) -> Tuple[Tuple[str, Union[str, int, None]], ...]:
        """Return the key path as a tuple of (kind, id_or_name) pairs.

        For incomplete keys, id_or_name may be None.
        """
        ...

    def flat(self) -> Tuple[Union[str, int, None], ...]:
        """Return the key path as a flat tuple: (kind1, id1, kind2, id2, ...).

        For incomplete keys, id values may be None.
        """
        ...

    @property
    def kind(self) -> str:
        """The kind of the entity this key refers to."""
        ...

    def string_id(self) -> Optional[str]:
        """Return the string ID of this key, or None if it has an integer ID or is incomplete."""
        ...

    def id(self) -> Optional[Union[str, int]]:
        """Return the string or integer ID of this key, or None if incomplete."""
        ...

    def integer_id(self) -> Optional[int]:
        """Return the integer ID of this key, or None if it has a string ID or is incomplete."""
        ...

    def namespace(self) -> Optional[str]:
        """Return the namespace for this key."""
        ...

    def project(self) -> str:
        """Return the project ID (app ID) for this key."""
        ...

    def database(self) -> Optional[str]:
        """Return the database ID for this key."""
        ...

    def parent(self) -> Optional[Key]:
        """Return the parent key, or None if this is a root key."""
        ...

    def root(self) -> Key:
        """Return the root key (topmost ancestor) of this key."""
        ...

    def urlsafe(self) -> bytes:
        """Return a URL-safe encoded representation of this key."""
        ...

    def serialized(self) -> bytes:
        """Return a serialized protocol buffer representation of this key."""
        ...

    def reference(self) -> Any:
        """Return the Reference protocol buffer for this key."""
        ...

    def to_legacy_urlsafe(self, location_prefix: Optional[str] = ...) -> bytes:
        """Convert key to legacy urlsafe format compatible with older datastore APIs."""
        ...

    @classmethod
    def from_legacy_urlsafe(cls, urlsafe: Union[bytes, str]) -> Key:
        """Construct a Key from a legacy urlsafe-encoded string."""
        ...

    def get(self, **ctx_options: Any) -> Optional[Any]:
        """Synchronously fetch the entity for this key.

        Returns the entity if it exists, None otherwise.
        """
        ...

    def get_async(self, **ctx_options: Any) -> Any:
        """Asynchronously fetch the entity for this key.

        Returns a Future that will resolve to the entity or None.
        """
        ...

    def delete(self, **ctx_options: Any) -> None:
        """Synchronously delete the entity for this key."""
        ...

    def delete_async(self, **ctx_options: Any) -> Any:
        """Asynchronously delete the entity for this key.

        Returns a Future that will resolve to None.
        """
        ...
