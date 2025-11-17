"""Type stubs for google.cloud.ndb.tasklets"""

from typing import Any, Callable, Coroutine, Generator, Generic, Iterable, List, Optional, TypeVar, Union

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)

class Return(StopIteration, Generic[_T]):
    """Return value from a tasklet."""
    value: _T
    def __init__(self, value: _T) -> None: ...

class Future(Generic[_T]):
    """Represents an asynchronous computation.

    Futures are returned by async methods and can be awaited to get the result.
    They can also be used with the tasklet decorator for generator-based async code.
    """

    def __init__(self) -> None: ...

    def set_result(self, result: _T) -> None:
        """Set the result of this future."""
        ...

    def set_exception(self, exception: BaseException) -> None:
        """Set an exception for this future."""
        ...

    def done(self) -> bool:
        """Return True if the future is done (has result or exception)."""
        ...

    def running(self) -> bool:
        """Return True if the future is currently running."""
        ...

    def wait(self) -> None:
        """Wait for the future to complete (blocking)."""
        ...

    def check_success(self) -> None:
        """Check if the future completed successfully, raise exception if not."""
        ...

    def get_result(self) -> _T:
        """Get the result of the future, blocking if necessary."""
        ...

    def get_exception(self) -> Optional[BaseException]:
        """Get the exception from the future, if any."""
        ...
    def get_traceback(self) -> Optional[Any]: ...
    def add_done_callback(self, callback: Callable[[Future[_T]], Any]) -> None: ...
    def remove_done_callback(self, callback: Callable[[Future[_T]], Any]) -> None: ...
    def cancel(self) -> None: ...
    def cancelled(self) -> bool: ...
    def result(self) -> _T: ...
    def exception(self) -> Optional[BaseException]: ...
    def __iter__(self) -> Generator[Future[_T], None, _T]: ...
    def __await__(self) -> Generator[Future[_T], None, _T]: ...

class MultiFuture(Future[List[_T]]):
    """Future that waits for multiple futures."""
    def __init__(self, futures: Iterable[Future[_T]]) -> None: ...

class QueueFuture(Future[List[_T]]):
    """Future that processes items from a queue."""
    ...

class SerialQueueFuture(Future[List[_T]]):
    """Future that processes items from a queue serially."""
    ...

class ReducingFuture(Future[_T]):
    """Future that reduces results."""
    def __init__(
        self,
        reducer: Callable[[_T, _T], _T],
        futures: Iterable[Future[_T]],
        initial: Optional[_T] = ...
    ) -> None: ...

def tasklet(func: Callable[..., Generator[Any, Any, _T]]) -> Callable[..., Future[_T]]:
    """Decorator for async generator functions that return Futures.

    Use 'yield' to wait for other futures in the generator body.
    """
    ...

def synctasklet(func: Callable[..., Generator[Any, Any, _T]]) -> Callable[..., _T]:
    """Like tasklet but waits for and returns the result synchronously."""
    ...

def toplevel(func: Callable[..., Any]) -> Callable[..., None]:
    """Decorator for top-level async entry points."""
    ...

def sleep(seconds: float) -> Future[None]:
    """Return a Future that completes after the specified number of seconds."""
    ...

def wait_all(futures: Iterable[Future[Any]]) -> None:
    """Wait for all futures to complete (blocking)."""
    ...

def wait_any(futures: Iterable[Future[Any]]) -> None:
    """Wait for any future to complete (blocking)."""
    ...

def make_context(**kwargs: Any) -> Any: ...  # Returns Context
def make_default_context(**kwargs: Any) -> Any: ...  # Returns Context
def set_context(context: Any) -> None: ...
def add_flow_exception(exc: BaseException) -> None: ...
