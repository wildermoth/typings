"""Type stubs for google.cloud.ndb._transaction"""

from typing import Any, Callable, Optional, TypeVar

from google.cloud.ndb import tasklets

_T = TypeVar("_T")

def in_transaction() -> bool:
    """Check if currently in a transaction."""
    ...

def transaction(
    callback: Callable[..., _T],
    retries: int = ...,
    **ctx_options: Any,
) -> _T:
    """Run a callback in a transaction."""
    ...

def transaction_async(
    callback: Callable[..., _T],
    retries: int = ...,
    **ctx_options: Any,
) -> tasklets.Future[_T]:
    """Run a callback in a transaction asynchronously."""
    ...

def transactional(
    retries: int = ...,
    **ctx_options: Any,
) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
    """Decorator to run a function in a transaction."""
    ...

def transactional_async(
    retries: int = ...,
    **ctx_options: Any,
) -> Callable[[Callable[..., _T]], Callable[..., tasklets.Future[_T]]]:
    """Decorator to run an async function in a transaction."""
    ...

def transactional_tasklet(
    retries: int = ...,
    **ctx_options: Any,
) -> Callable[[Callable[..., _T]], Callable[..., tasklets.Future[_T]]]:
    """Decorator to run a tasklet in a transaction."""
    ...

def non_transactional(
    allow_existing: bool = ...,
) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
    """Decorator to run a function outside of a transaction."""
    ...
