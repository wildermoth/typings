"""Type stubs for google.cloud.datastore.key"""

from typing import Any, Dict, List, Optional, Tuple, Union

from google.cloud.datastore_v1.types import entity as _entity_pb2

class Key:
    """An immutable representation of a datastore Key.

    Keys are composed of a path of alternating kind and ID/name values.
    Example: Key('ParentKind', 'parent_name', 'ChildKind', 1234, project='my-project')
    """

    _flat_path: Tuple[Union[str, int], ...]
    _parent: Optional[Key]
    _namespace: Optional[str]
    _database: Optional[str]
    _project: str
    _path: List[Dict[str, Any]]

    def __init__(
        self,
        *path_args: Union[str, int],
        parent: Optional[Key] = ...,
        namespace: Optional[str] = ...,
        project: Optional[str] = ...,
        database: Optional[str] = ...
    ) -> None: ...

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __repr__(self) -> str: ...

    @staticmethod
    def _parse_path(path_args: Tuple[Union[str, int], ...]) -> List[Dict[str, Any]]: ...

    def _combine_args(self) -> List[Dict[str, Any]]: ...
    def _clone(self) -> Key: ...
    def _make_parent(self) -> Optional[Key]: ...

    def completed_key(self, id_or_name: Union[str, int]) -> Key:
        """Create a completed key by adding an ID or name to this partial key."""
        ...

    def to_protobuf(self) -> _entity_pb2.Key:
        """Convert this key to a protobuf representation."""
        ...

    def to_legacy_urlsafe(self, location_prefix: Optional[str] = ...) -> bytes:
        """Convert to legacy urlsafe format for compatibility with older APIs."""
        ...

    @classmethod
    def from_legacy_urlsafe(cls, urlsafe: Union[bytes, str]) -> Key:
        """Create a Key from a legacy urlsafe-encoded string."""
        ...

    @property
    def is_partial(self) -> bool:
        """True if this key is incomplete (lacks an ID or name)."""
        ...

    @property
    def database(self) -> Optional[str]:
        """The database ID for this key."""
        ...

    @property
    def namespace(self) -> Optional[str]:
        """The namespace for this key."""
        ...

    @property
    def path(self) -> List[Dict[str, Any]]:
        """The path of this key as a list of dicts."""
        ...

    @property
    def flat_path(self) -> Tuple[Union[str, int], ...]:
        """The path as a flat tuple of alternating kinds and IDs."""
        ...

    @property
    def kind(self) -> str:
        """The kind of the entity this key refers to."""
        ...

    @property
    def id(self) -> Optional[int]:
        """The integer ID, or None if this key has a string name or is partial."""
        ...

    @property
    def name(self) -> Optional[str]:
        """The string name, or None if this key has an integer ID or is partial."""
        ...

    @property
    def id_or_name(self) -> Optional[Union[int, str]]:
        """The ID or name, or None if this is a partial key."""
        ...

    @property
    def project(self) -> str:
        """The project ID (app ID) for this key."""
        ...

    @property
    def parent(self) -> Optional[Key]:
        """The parent key, or None if this is a root entity."""
        ...

def _validate_project(project: Optional[str], parent: Optional[Key]) -> Optional[str]: ...
def _clean_app(app_str: str) -> str: ...
def _get_empty(value: Any, empty_value: Any) -> Optional[Any]: ...
def _check_database_id(database_id: Optional[str]) -> None: ...
def _add_id_or_name(flat_path: List[Union[str, int]], element_pb: Any, empty_allowed: bool) -> None: ...
def _get_flat_path(path_pb: Any) -> Tuple[Union[str, int], ...]: ...
def _to_legacy_path(dict_path: List[Dict[str, Any]]) -> Any: ...
