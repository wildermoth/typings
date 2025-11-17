"""Type stubs for google.cloud.datastore.aggregation"""

from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
import datetime

from google.api_core import page_iterator, retry as retry_module
from google.cloud.datastore.query import Query
from google.cloud.datastore.query_profile import ExplainMetrics, ExplainOptions
from google.cloud.datastore_v1.types import query as query_pb2

class BaseAggregation(ABC):
    """Base class representing an Aggregation operation in Datastore"""

    alias: Optional[str]

    def __init__(self, alias: Optional[str] = ...) -> None: ...

    @abstractmethod
    def _to_pb(self) -> query_pb2.AggregationQuery.Aggregation: ...

class CountAggregation(BaseAggregation):
    """Representation of a "Count" aggregation query."""

    def __init__(self, alias: Optional[str] = ...) -> None: ...
    def _to_pb(self) -> query_pb2.AggregationQuery.Aggregation: ...

class SumAggregation(BaseAggregation):
    """Representation of a "Sum" aggregation query."""

    property_ref: str

    def __init__(self, property_ref: str, alias: Optional[str] = ...) -> None: ...
    def _to_pb(self) -> query_pb2.AggregationQuery.Aggregation: ...

class AvgAggregation(BaseAggregation):
    """Representation of a "Avg" aggregation query."""

    property_ref: str

    def __init__(self, property_ref: str, alias: Optional[str] = ...) -> None: ...
    def _to_pb(self) -> query_pb2.AggregationQuery.Aggregation: ...

class AggregationResult:
    """A class representing result from Aggregation Query"""

    alias: str
    value: Union[int, float]

    def __init__(self, alias: str, value: Union[int, float]) -> None: ...
    def __repr__(self) -> str: ...

class AggregationQuery:
    """An Aggregation query against the Cloud Datastore."""

    _client: Any
    _nested_query: Query
    _aggregations: List[BaseAggregation]
    _explain_options: Optional[ExplainOptions]

    def __init__(
        self,
        client: Any,
        query: Query,
        explain_options: Optional[ExplainOptions] = ...
    ) -> None: ...

    @property
    def project(self) -> str: ...

    @property
    def namespace(self) -> Optional[str]: ...

    def _to_pb(self) -> query_pb2.AggregationQuery: ...

    def count(self, alias: Optional[str] = ...) -> AggregationQuery: ...
    def sum(self, property_ref: str, alias: Optional[str] = ...) -> AggregationQuery: ...
    def avg(self, property_ref: str, alias: Optional[str] = ...) -> AggregationQuery: ...
    def add_aggregation(self, aggregation: BaseAggregation) -> None: ...
    def add_aggregations(self, aggregations: List[BaseAggregation]) -> None: ...

    def fetch(
        self,
        client: Optional[Any] = ...,
        limit: Optional[int] = ...,
        eventual: bool = ...,
        retry: Optional[retry_module.Retry] = ...,
        timeout: Optional[float] = ...,
        read_time: Optional[datetime.datetime] = ...
    ) -> AggregationResultIterator: ...

class AggregationResultIterator(page_iterator.Iterator):
    """Represent the state of a given execution of an AggregationQuery."""

    _aggregation_query: AggregationQuery
    _eventual: bool
    _retry: Optional[retry_module.Retry]
    _timeout: Optional[float]
    _read_time: Optional[datetime.datetime]
    _limit: Optional[int]
    _explain_metrics: Optional[ExplainMetrics]
    _more_results: bool

    def __init__(
        self,
        aggregation_query: AggregationQuery,
        client: Any,
        limit: Optional[int] = ...,
        eventual: bool = ...,
        retry: Optional[retry_module.Retry] = ...,
        timeout: Optional[float] = ...,
        read_time: Optional[datetime.datetime] = ...
    ) -> None: ...

    def _build_protobuf(self) -> query_pb2.AggregationQuery: ...
    def _process_query_results(self, response_pb: Any) -> List[Any]: ...
    def _next_page(self) -> Optional[page_iterator.Page]: ...

    @property
    def explain_metrics(self) -> ExplainMetrics: ...

def _item_to_aggregation_result(iterator: page_iterator.Iterator, pb: Any) -> List[AggregationResult]: ...
