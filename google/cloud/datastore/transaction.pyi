"""Type stubs for google.cloud.datastore.transaction"""

from typing import Any, Dict, Optional
import datetime

from google.cloud.datastore.batch import Batch
from google.cloud.datastore.entity import Entity
from google.cloud.datastore_v1.types import TransactionOptions
from google.api_core import retry as retry_module

class Transaction(Batch):
    """An abstraction representing datastore Transactions."""

    _id: Optional[bytes]
    _begin_later: bool
    _options: TransactionOptions

    def __init__(
        self,
        client: Any,
        read_only: bool = ...,
        read_time: Optional[datetime.datetime] = ...,
        begin_later: bool = ...
    ) -> None: ...

    @property
    def id(self) -> Optional[bytes]: ...

    def current(self) -> Optional[Transaction]: ...

    def begin(
        self,
        retry: Optional[retry_module.Retry] = ...,
        timeout: Optional[float] = ...
    ) -> None: ...

    def _begin_with_id(self, transaction_id: bytes) -> None: ...

    def rollback(
        self,
        retry: Optional[retry_module.Retry] = ...,
        timeout: Optional[float] = ...
    ) -> None: ...

    def commit(
        self,
        retry: Optional[retry_module.Retry] = ...,
        timeout: Optional[float] = ...
    ) -> None: ...

    def put(self, entity: Entity) -> None: ...

    def __enter__(self) -> Transaction: ...

    def _allow_mutations(self) -> bool: ...

def _make_retry_timeout_kwargs(
    retry: Optional[retry_module.Retry],
    timeout: Optional[float]
) -> Dict[str, Any]: ...
