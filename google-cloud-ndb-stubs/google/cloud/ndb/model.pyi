"""Type stubs for google.cloud.ndb.model"""

from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)
import datetime

from google.cloud.ndb import key as key_module
from google.cloud.ndb import query as query_module
from google.cloud.ndb import tasklets
from google.cloud.ndb import exceptions

_T = TypeVar("_T")
_ModelT = TypeVar("_ModelT", bound="Model")

# Exception classes
class KindError(exceptions.BadValueError): ...
class InvalidPropertyError(exceptions.Error): ...
class BadProjectionError(exceptions.Error): ...
class UnprojectedPropertyError(exceptions.Error): ...
class ReadonlyPropertyError(exceptions.Error): ...
class ComputedPropertyError(ReadonlyPropertyError): ...
class UserNotFoundError(exceptions.Error): ...

class Rollback(exceptions.Rollback): ...

# Special types
class BlobKey:
    """A blob key for Blobstore."""
    def __init__(self, blob_key: str) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

class GeoPt:
    """A geographical point (latitude, longitude)."""
    lat: float
    lon: float
    def __init__(self, lat: float, lon: float) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

class User:
    """A user with an email address and optional user ID."""
    def __init__(
        self,
        email: Optional[str] = ...,
        _auth_domain: Optional[str] = ...,
        _user_id: Optional[str] = ...,
    ) -> None: ...
    def email(self) -> Optional[str]: ...
    def auth_domain(self) -> Optional[str]: ...
    def user_id(self) -> Optional[str]: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

# Index types
class IndexState:
    """State of a datastore index."""
    ERROR: str
    DELETING: str
    SERVING: str
    BUILDING: str

class IndexProperty:
    """Property of a datastore index."""
    name: str
    direction: str
    def __init__(self, name: str, direction: str) -> None: ...

class Index:
    """A datastore index."""
    kind: str
    properties: List[IndexProperty]
    ancestor: bool
    state: str
    def __init__(
        self,
        kind: str,
        properties: List[IndexProperty],
        ancestor: bool,
        state: str = ...,
    ) -> None: ...

# Property base classes
class Property(Generic[_T]):
    """Base class for all property types."""

    _name: str
    _indexed: bool
    _repeated: bool
    _required: bool
    _default: Optional[Union[_T, Callable[[], _T]]]
    _choices: Optional[Sequence[_T]]
    _validator: Optional[Callable[[Property[_T], _T], _T]]
    _verbose_name: Optional[str]
    _write_empty_list: bool

    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Union[_T, Callable[[], _T]]] = ...,
        choices: Optional[Sequence[_T]] = ...,
        validator: Optional[Callable[[Property[_T], _T], _T]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

    def __get__(self, instance: Optional[Model], owner: Type[Model]) -> Union[_T, Property[_T]]: ...
    @overload
    def __set__(self, instance: None, value: None) -> None: ...
    @overload
    def __set__(self, instance: Model, value: _T) -> None: ...
    def __delete__(self, instance: Model) -> None: ...

    def _has_value(self, entity: Model, rest: Optional[List[str]] = ...) -> bool: ...
    def _retrieve_value(self, entity: Model, default: _T = ...) -> _T: ...
    def _set_value(self, entity: Model, value: _T) -> None: ...
    def _delete_value(self, entity: Model) -> None: ...

    def _validate(self, value: _T) -> _T: ...
    def _to_base_type(self, value: _T) -> Any: ...
    def _from_base_type(self, value: Any) -> _T: ...
    def _prepare_for_put(self, entity: Model) -> None: ...

    def __eq__(self, value: Any) -> query_module.FilterNode: ...
    def __ne__(self, value: Any) -> query_module.FilterNode: ...
    def __lt__(self, value: Any) -> query_module.FilterNode: ...
    def __le__(self, value: Any) -> query_module.FilterNode: ...
    def __gt__(self, value: Any) -> query_module.FilterNode: ...
    def __ge__(self, value: Any) -> query_module.FilterNode: ...
    def IN(self, value: Iterable[Any]) -> query_module.FilterNode: ...

class ModelKey(Property[key_module.Key]):
    """Special property for entity keys."""
    ...

class ModelAttribute:
    """Base class for model attributes."""
    ...

class ModelAdapter:
    """Adapter for model serialization."""
    ...

# Concrete property types
class BooleanProperty(Property[bool]):
    """A boolean property."""
    ...

class IntegerProperty(Property[int]):
    """An integer property."""
    ...

class FloatProperty(Property[float]):
    """A floating point property."""
    ...

class StringProperty(Property[str]):
    """A short string property (up to 1500 bytes)."""
    ...

class TextProperty(Property[str]):
    """An unlimited text property (unindexed)."""
    ...

class BlobProperty(Property[bytes]):
    """A binary data property (unindexed)."""
    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        compressed: bool = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Union[bytes, Callable[[], bytes]]] = ...,
        choices: Optional[Sequence[bytes]] = ...,
        validator: Optional[Callable[[BlobProperty, bytes], bytes]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class DateTimeProperty(Property[datetime.datetime]):
    """A datetime property."""
    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        auto_now: bool = ...,
        auto_now_add: bool = ...,
        tzinfo: Optional[datetime.tzinfo] = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Union[datetime.datetime, Callable[[], datetime.datetime]]] = ...,
        choices: Optional[Sequence[datetime.datetime]] = ...,
        validator: Optional[Callable[[DateTimeProperty, datetime.datetime], datetime.datetime]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class DateProperty(Property[datetime.date]):
    """A date property."""
    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        auto_now: bool = ...,
        auto_now_add: bool = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Union[datetime.date, Callable[[], datetime.date]]] = ...,
        choices: Optional[Sequence[datetime.date]] = ...,
        validator: Optional[Callable[[DateProperty, datetime.date], datetime.date]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class TimeProperty(Property[datetime.time]):
    """A time property."""
    ...

class GeoPtProperty(Property[GeoPt]):
    """A geographical point property."""
    ...

class KeyProperty(Property[key_module.Key]):
    """A key reference property."""
    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        kind: Optional[Union[str, Type[Model]]] = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Union[key_module.Key, Callable[[], key_module.Key]]] = ...,
        choices: Optional[Sequence[key_module.Key]] = ...,
        validator: Optional[Callable[[KeyProperty, key_module.Key], key_module.Key]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class BlobKeyProperty(Property[BlobKey]):
    """A blobstore key property."""
    ...

class UserProperty(Property[User]):
    """A user property."""
    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        auto_current_user: bool = ...,
        auto_current_user_add: bool = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Union[User, Callable[[], User]]] = ...,
        choices: Optional[Sequence[User]] = ...,
        validator: Optional[Callable[[UserProperty, User], User]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class StructuredProperty(Property[_ModelT]):
    """A property that stores a structured sub-entity."""
    def __init__(
        self,
        model_class: Type[_ModelT],
        name: Optional[str] = ...,
        *,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Union[_ModelT, Callable[[], _ModelT]]] = ...,
        choices: Optional[Sequence[_ModelT]] = ...,
        validator: Optional[Callable[[StructuredProperty[_ModelT], _ModelT], _ModelT]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class LocalStructuredProperty(StructuredProperty[_ModelT]):
    """A property that stores a structured sub-entity as an opaque blob."""
    def __init__(
        self,
        model_class: Type[_ModelT],
        name: Optional[str] = ...,
        *,
        compressed: bool = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Union[_ModelT, Callable[[], _ModelT]]] = ...,
        choices: Optional[Sequence[_ModelT]] = ...,
        validator: Optional[Callable[[LocalStructuredProperty[_ModelT], _ModelT], _ModelT]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class GenericProperty(Property[Any]):
    """A property that can store any type."""
    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        compressed: bool = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Any] = ...,
        choices: Optional[Sequence[Any]] = ...,
        validator: Optional[Callable[[GenericProperty, Any], Any]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class ComputedProperty(Property[_T]):
    """A property whose value is computed from other properties."""
    def __init__(
        self,
        func: Callable[[Model], _T],
        name: Optional[str] = ...,
        *,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        verbose_name: Optional[str] = ...,
    ) -> None: ...

class JsonProperty(Property[Any]):
    """A property that stores JSON-serializable values."""
    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        compressed: bool = ...,
        json_type: Optional[type] = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Any] = ...,
        choices: Optional[Sequence[Any]] = ...,
        validator: Optional[Callable[[JsonProperty, Any], Any]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

class PickleProperty(Property[Any]):
    """A property that stores pickled values."""
    def __init__(
        self,
        name: Optional[str] = ...,
        *,
        compressed: bool = ...,
        indexed: Optional[bool] = ...,
        repeated: bool = ...,
        required: bool = ...,
        default: Optional[Any] = ...,
        choices: Optional[Sequence[Any]] = ...,
        validator: Optional[Callable[[PickleProperty, Any], Any]] = ...,
        verbose_name: Optional[str] = ...,
        write_empty_list: bool = ...,
    ) -> None: ...

# Metaclass
class MetaModel(type):
    """Metaclass for Model classes."""
    ...

# Model class
class Model:
    """Base class for datastore models."""

    _properties: Dict[str, Property[Any]]
    _has_repeated: bool
    _kind_map: Dict[str, Type[Model]]

    key: key_module.Key
    _key: key_module.Key

    def __init__(
        self,
        *,
        key: Optional[key_module.Key] = ...,
        id: Optional[Union[str, int]] = ...,
        parent: Optional[key_module.Key] = ...,
        namespace: Optional[str] = ...,
        project: Optional[str] = ...,
        app: Optional[str] = ...,
        database: Optional[str] = ...,
        projection: Optional[Iterable[str]] = ...,
        **kwargs: Any,
    ) -> None: ...

    @classmethod
    def _get_kind(cls) -> str:
        """Get the datastore kind for this model class."""
        ...

    @classmethod
    def _class_name(cls) -> str: ...

    @classmethod
    def _default_filters(cls) -> Tuple[query_module.FilterNode, ...]: ...

    def _prepare_for_put(self) -> None: ...
    def _pre_put_hook(self) -> None: ...
    def _post_put_hook(self, future: tasklets.Future[key_module.Key]) -> None: ...
    def _pre_delete_hook(self) -> None: ...
    def _post_delete_hook(self, future: tasklets.Future[None]) -> None: ...
    def _pre_get_hook(cls, key: key_module.Key) -> None: ...
    def _post_get_hook(cls, key: key_module.Key, future: tasklets.Future[Optional[Model]]) -> None: ...

    def put(self, **ctx_options: Any) -> key_module.Key: ...
    def put_async(self, **ctx_options: Any) -> tasklets.Future[key_module.Key]: ...

    @classmethod
    def get_by_id(
        cls: Type[_ModelT],
        id: Union[str, int],
        parent: Optional[key_module.Key] = ...,
        namespace: Optional[str] = ...,
        app: Optional[str] = ...,
        project: Optional[str] = ...,
        database: Optional[str] = ...,
        **ctx_options: Any,
    ) -> Optional[_ModelT]: ...

    @classmethod
    def get_by_id_async(
        cls: Type[_ModelT],
        id: Union[str, int],
        parent: Optional[key_module.Key] = ...,
        namespace: Optional[str] = ...,
        app: Optional[str] = ...,
        project: Optional[str] = ...,
        database: Optional[str] = ...,
        **ctx_options: Any,
    ) -> tasklets.Future[Optional[_ModelT]]: ...

    @classmethod
    def get_or_insert(
        cls: Type[_ModelT],
        name: str,
        parent: Optional[key_module.Key] = ...,
        namespace: Optional[str] = ...,
        app: Optional[str] = ...,
        project: Optional[str] = ...,
        database: Optional[str] = ...,
        **kwargs: Any,
    ) -> _ModelT: ...

    @classmethod
    def get_or_insert_async(
        cls: Type[_ModelT],
        name: str,
        parent: Optional[key_module.Key] = ...,
        namespace: Optional[str] = ...,
        app: Optional[str] = ...,
        project: Optional[str] = ...,
        database: Optional[str] = ...,
        **kwargs: Any,
    ) -> tasklets.Future[_ModelT]: ...

    @classmethod
    def allocate_ids(
        cls,
        size: Optional[int] = ...,
        max: Optional[int] = ...,
        parent: Optional[key_module.Key] = ...,
        **ctx_options: Any,
    ) -> Tuple[key_module.Key, key_module.Key]: ...

    @classmethod
    def allocate_ids_async(
        cls,
        size: Optional[int] = ...,
        max: Optional[int] = ...,
        parent: Optional[key_module.Key] = ...,
        **ctx_options: Any,
    ) -> tasklets.Future[Tuple[key_module.Key, key_module.Key]]: ...

    @classmethod
    def query(cls: Type[_ModelT], *args: query_module.Node, **kwargs: Any) -> query_module.Query: ...

    def populate(self, **kwargs: Any) -> None: ...
    def has_complete_key(self) -> bool: ...
    def to_dict(
        self,
        include: Optional[Union[Iterable[str], Dict[str, Any]]] = ...,
        exclude: Optional[Union[Iterable[str], Dict[str, Any]]] = ...,
    ) -> Dict[str, Any]: ...

    @classmethod
    def _lookup_model(
        cls,
        kinds: Iterable[str],
        default_model: Optional[Type[Model]] = ...,
    ) -> Dict[str, Type[Model]]: ...

class Expando(Model):
    """A model with dynamic properties."""
    ...

# Top-level functions
def get_multi(
    keys: Iterable[key_module.Key],
    **ctx_options: Any,
) -> List[Optional[Model]]: ...

def get_multi_async(
    keys: Iterable[key_module.Key],
    **ctx_options: Any,
) -> tasklets.Future[List[Optional[Model]]]: ...

def put_multi(
    entities: Iterable[Model],
    **ctx_options: Any,
) -> List[key_module.Key]: ...

def put_multi_async(
    entities: Iterable[Model],
    **ctx_options: Any,
) -> tasklets.Future[List[key_module.Key]]: ...

def delete_multi(
    keys: Iterable[key_module.Key],
    **ctx_options: Any,
) -> None: ...

def delete_multi_async(
    keys: Iterable[key_module.Key],
    **ctx_options: Any,
) -> tasklets.Future[None]: ...

def get_indexes(**ctx_options: Any) -> List[Index]: ...
def get_indexes_async(**ctx_options: Any) -> tasklets.Future[List[Index]]: ...

def make_connection(config: Optional[Any] = ...) -> Any: ...
