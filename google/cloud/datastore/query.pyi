"""Type stubs for google.cloud.datastore.query"""

from typing import Any, Dict, Iterable, Iterator as TypingIterator, List, Optional, Sequence, Tuple, Union
from abc import ABC, abstractmethod
import datetime

from google.api_core import page_iterator, retry as retry_module
from google.cloud.datastore.entity import Entity
from google.cloud.datastore.key import Key
from google.cloud.datastore.query_profile import ExplainMetrics, ExplainOptions
from google.cloud.datastore_v1.types import query as query_pb2

KEY_PROPERTY_NAME: str

class BaseFilter(ABC):
    """Base class for Filters"""

    @abstractmethod
    def build_pb(self, container_pb: Optional[Any] = ...) -> Any: ...

class PropertyFilter(BaseFilter):
    """Class representation of a Property Filter"""

    property_name: str
    operator: str
    value: Any

    def __init__(self, property_name: str, operator: str, value: Any) -> None: ...
    def build_pb(self, container_pb: Optional[Any] = ...) -> Any: ...
    def __repr__(self) -> str: ...

class BaseCompositeFilter(BaseFilter):
    """Base class for a Composite Filter. (either OR or AND)."""

    operation: int
    filters: List[Union[BaseFilter, Tuple[str, str, Any]]]

    def __init__(
        self,
        operation: int = ...,
        filters: Optional[List[Union[BaseFilter, Tuple[str, str, Any]]]] = ...
    ) -> None: ...
    def __repr__(self) -> str: ...
    def build_pb(self, container_pb: Optional[Any] = ...) -> Any: ...

class Or(BaseCompositeFilter):
    """Class representation of an OR Filter."""

    def __init__(self, filters: List[Union[BaseFilter, Tuple[str, str, Any]]]) -> None: ...

class And(BaseCompositeFilter):
    """Class representation of an AND Filter."""

    def __init__(self, filters: List[Union[BaseFilter, Tuple[str, str, Any]]]) -> None: ...

class Query:
    """A Query against the Cloud Datastore.

    Build queries by adding filters, projection, and ordering. Then fetch
    results using the fetch() or iterator methods.

    Example:
        query = client.query(kind='Task')
        query.add_filter('done', '=', False)
        results = list(query.fetch())
    """

    OPERATORS: Dict[str, int]

    _client: Any
    _kind: Optional[str]
    _project: Optional[str]
    _namespace: Optional[str]
    _explain_options: Optional[ExplainOptions]
    _ancestor: Optional[Key]
    _filters: List[Union[BaseFilter, Tuple[str, str, Any]]]
    _projection: Sequence[str]
    _order: Sequence[str]
    _distinct_on: Sequence[str]

    def __init__(
        self,
        client: Any,
        kind: Optional[str] = ...,
        project: Optional[str] = ...,
        namespace: Optional[str] = ...,
        ancestor: Optional[Key] = ...,
        filters: Union[Sequence[Union[BaseFilter, Tuple[str, str, Any]]], Tuple[()]] = ...,
        projection: Union[Sequence[str], Tuple[()]] = ...,
        order: Union[Sequence[str], Tuple[()]] = ...,
        distinct_on: Union[Sequence[str], Tuple[()]] = ...,
        explain_options: Optional[ExplainOptions] = ...
    ) -> None: ...

    @property
    def project(self) -> str: ...

    @property
    def namespace(self) -> Optional[str]: ...

    @namespace.setter
    def namespace(self, value: str) -> None: ...

    @property
    def kind(self) -> Optional[str]: ...

    @kind.setter
    def kind(self, value: str) -> None: ...

    @property
    def ancestor(self) -> Optional[Key]: ...

    @ancestor.setter
    def ancestor(self, value: Key) -> None: ...

    @ancestor.deleter
    def ancestor(self) -> None: ...

    @property
    def filters(self) -> List[Union[BaseFilter, Tuple[str, str, Any]]]: ...

    def add_filter(
        self,
        property_name: Optional[str] = ...,
        operator: Optional[str] = ...,
        value: Any = ...,
        *,
        filter: Optional[BaseFilter] = ...
    ) -> Query: ...

    @property
    def projection(self) -> Sequence[str]: ...

    @projection.setter
    def projection(self, projection: Union[str, Sequence[str]]) -> None: ...

    def keys_only(self) -> None: ...
    def key_filter(self, key: Key, operator: str = ...) -> None: ...

    @property
    def order(self) -> Sequence[str]: ...

    @order.setter
    def order(self, value: Union[str, Sequence[str]]) -> None: ...

    @property
    def distinct_on(self) -> Sequence[str]: ...

    @distinct_on.setter
    def distinct_on(self, value: Union[str, Sequence[str]]) -> None: ...

    def fetch(
        self,
        limit: Optional[int] = ...,
        offset: int = ...,
        start_cursor: Optional[bytes] = ...,
        end_cursor: Optional[bytes] = ...,
        client: Optional[Any] = ...,
        eventual: bool = ...,
        retry: Optional[retry_module.Retry] = ...,
        timeout: Optional[float] = ...,
        read_time: Optional[datetime.datetime] = ...
    ) -> Iterator: ...

class Iterator(page_iterator.Iterator):
    """Represent the state of a given execution of a Query."""

    next_page_token: Optional[str]

    _query: Query
    _offset: Optional[int]
    _end_cursor: Optional[bytes]
    _eventual: bool
    _retry: Optional[retry_module.Retry]
    _timeout: Optional[float]
    _read_time: Optional[datetime.datetime]
    _explain_metrics: Optional[ExplainMetrics]
    _more_results: bool
    _skipped_results: int

    def __init__(
        self,
        query: Query,
        client: Any,
        limit: Optional[int] = ...,
        offset: Optional[int] = ...,
        start_cursor: Optional[bytes] = ...,
        end_cursor: Optional[bytes] = ...,
        eventual: bool = ...,
        retry: Optional[retry_module.Retry] = ...,
        timeout: Optional[float] = ...,
        read_time: Optional[datetime.datetime] = ...
    ) -> None: ...

    def _build_protobuf(self) -> query_pb2.Query: ...
    def _process_query_results(self, response_pb: Any) -> List[Any]: ...
    def _next_page(self) -> Optional[page_iterator.Page]: ...

    @property
    def explain_metrics(self) -> ExplainMetrics: ...

def _pb_from_query(query: Query) -> query_pb2.Query: ...
def _item_to_entity(iterator: page_iterator.Iterator, entity_pb: Any) -> Entity: ...
