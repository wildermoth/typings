"""Type stubs for google.cloud.ndb.query"""

from typing import Any, Callable, Generic, Iterable, Iterator, List, Optional, Tuple, Type, TypeVar, Union

from google.cloud.ndb import key as key_module
from google.cloud.ndb import model as model_module
from google.cloud.ndb import tasklets

_ModelT = TypeVar("_ModelT", bound="model_module.Model")

# Query node classes
class Node:
    """Base class for query filter nodes."""
    def __eq__(self, other: object) -> bool: ...  # type: ignore[override]
    def __ne__(self, other: object) -> bool: ...  # type: ignore[override]

class FilterNode(Node):
    """A filter expression in a query."""
    def __init__(self, name: str, opsymbol: str, value: Any) -> None: ...
    def __repr__(self) -> str: ...

class PostFilterNode(Node):
    """A post-filter node."""
    def __init__(self, predicate: Callable[[model_module.Model], bool]) -> None: ...

class ConjunctionNode(Node):
    """A conjunction (AND) of filter nodes."""
    def __init__(self, *nodes: Node) -> None: ...
    def __repr__(self) -> str: ...

class DisjunctionNode(Node):
    """A disjunction (OR) of filter nodes."""
    def __init__(self, *nodes: Node) -> None: ...
    def __repr__(self) -> str: ...

class FalseNode(Node):
    """A node that always evaluates to False."""
    ...

class ParameterNode(Node):
    """A parameter placeholder in a query."""
    def __init__(self, prop: model_module.Property[Any]) -> None: ...

class Parameter:
    """A query parameter."""
    def __init__(self, key: Union[str, int]) -> None: ...

class ParameterizedThing:
    """Base class for parameterized query components."""
    ...

class ParameterizedFunction(ParameterizedThing):
    """A parameterized function in a query."""
    ...

class RepeatedStructuredPropertyPredicate:
    """Predicate for repeated structured properties."""
    def __init__(
        self,
        name: str,
        match_keys: List[str],
        match_values: List[Any],
        **kwargs: Any,
    ) -> None: ...

# Constants
AND: Type[ConjunctionNode]
OR: Type[DisjunctionNode]

# Cursor
class Cursor:
    """A query cursor for pagination."""
    def __init__(self, cursor: bytes = ...) -> None: ...
    def to_bytes(self) -> bytes: ...
    def urlsafe(self) -> bytes: ...
    @classmethod
    def from_bytes(cls, urlsafe: bytes) -> Cursor: ...

# Query iterator
class QueryIterator(Iterator[_ModelT]):
    """Iterator for query results."""
    def __init__(
        self,
        query: Query,
        **kwargs: Any,
    ) -> None: ...

    def __iter__(self) -> QueryIterator[_ModelT]: ...
    def __next__(self) -> _ModelT: ...
    def has_next(self) -> bool: ...
    def has_next_async(self) -> tasklets.Future[bool]: ...
    def probably_has_next(self) -> bool: ...
    def cursor_before(self) -> Optional[Cursor]: ...
    def cursor_after(self) -> Optional[Cursor]: ...
    def index_list(self) -> List[Any]: ...

# Query options
class QueryOptions:
    """Options for query execution."""
    def __init__(
        self,
        *,
        keys_only: Optional[bool] = ...,
        projection: Optional[Iterable[str]] = ...,
        offset: Optional[int] = ...,
        limit: Optional[int] = ...,
        batch_size: Optional[int] = ...,
        prefetch_size: Optional[int] = ...,
        produce_cursors: Optional[bool] = ...,
        start_cursor: Optional[Cursor] = ...,
        end_cursor: Optional[Cursor] = ...,
        deadline: Optional[float] = ...,
        read_consistency: Optional[Any] = ...,
        read_policy: Optional[Any] = ...,
        timeout: Optional[float] = ...,
        use_cache: Optional[bool] = ...,
        use_global_cache: Optional[bool] = ...,
        global_cache_timeout: Optional[int] = ...,
        use_datastore: Optional[bool] = ...,
        memcache_timeout: Optional[int] = ...,
        max_memcache_items: Optional[int] = ...,
        read_time: Optional[Any] = ...,
    ) -> None: ...

# Main Query class
class Query(Generic[_ModelT]):
    """A query for datastore entities."""

    def __init__(
        self,
        kind: Optional[Union[str, Type[_ModelT]]] = ...,
        *,
        ancestor: Optional[key_module.Key] = ...,
        filters: Optional[Node] = ...,
        orders: Optional[Any] = ...,
        app: Optional[str] = ...,
        namespace: Optional[str] = ...,
        projection: Optional[Iterable[str]] = ...,
        distinct: Optional[bool] = ...,
        group_by: Optional[Iterable[str]] = ...,
        default_options: Optional[QueryOptions] = ...,
        project: Optional[str] = ...,
        database: Optional[str] = ...,
    ) -> None: ...

    def filter(self, *filters: Node) -> Query[_ModelT]: ...
    def order(self, *props: Union[model_module.Property[Any], str]) -> Query[_ModelT]: ...

    def analyze(self) -> List[Any]: ...

    def fetch(
        self,
        limit: Optional[int] = ...,
        **ctx_options: Any,
    ) -> List[_ModelT]: ...

    def fetch_async(
        self,
        limit: Optional[int] = ...,
        **ctx_options: Any,
    ) -> tasklets.Future[List[_ModelT]]: ...

    def fetch_page(
        self,
        page_size: int,
        start_cursor: Optional[Cursor] = ...,
        **ctx_options: Any,
    ) -> Tuple[List[_ModelT], Optional[Cursor], bool]: ...

    def fetch_page_async(
        self,
        page_size: int,
        start_cursor: Optional[Cursor] = ...,
        **ctx_options: Any,
    ) -> tasklets.Future[Tuple[List[_ModelT], Optional[Cursor], bool]]: ...

    def get(self, **ctx_options: Any) -> Optional[_ModelT]: ...
    def get_async(self, **ctx_options: Any) -> tasklets.Future[Optional[_ModelT]]: ...

    def count(
        self,
        limit: Optional[int] = ...,
        **ctx_options: Any,
    ) -> int: ...

    def count_async(
        self,
        limit: Optional[int] = ...,
        **ctx_options: Any,
    ) -> tasklets.Future[int]: ...

    def iter(
        self,
        **ctx_options: Any,
    ) -> QueryIterator[_ModelT]: ...

    def map(
        self,
        callback: Callable[[_ModelT], Any],
        **ctx_options: Any,
    ) -> List[Any]: ...

    def map_async(
        self,
        callback: Callable[[_ModelT], Any],
        **ctx_options: Any,
    ) -> tasklets.Future[List[Any]]: ...

    @property
    def kind(self) -> Optional[str]: ...

    @property
    def ancestor(self) -> Optional[key_module.Key]: ...

    @property
    def filters(self) -> Optional[Node]: ...

    @property
    def is_distinct(self) -> bool: ...

    @property
    def projection(self) -> Optional[Tuple[str, ...]]: ...

def gql(query_string: str, *args: Any, **kwargs: Any) -> Query[Any]: ...
