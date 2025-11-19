"""Type stubs for pytest"""
from typing import Any, Callable, TypeVar, NoReturn

_T = TypeVar("_T")

# Fixture decorator - returns the function itself (for ty compatibility)
@overload
def fixture(func: _T) -> _T: ...
@overload
def fixture(*, autouse: bool = False, scope: str = "function", params: Any = None) -> Callable[[_T], _T]: ...

def fixture(func: _T | None = None, *, autouse: bool = False, scope: str = "function", params: Any = None) -> _T | Callable[[_T], _T]: ...

# Mark decorators
class MarkDecorator:
    def __call__(self, func: _T) -> _T: ...

class Mark:
    parametrize: Callable[..., MarkDecorator]
    usefixtures: Callable[..., MarkDecorator]

mark: Mark

# Other common pytest functions
def raises(exc: type[BaseException], *args: Any, **kwargs: Any) -> Any: ...
def fail(msg: str = "", pytrace: bool = True) -> NoReturn: ...
def skip(msg: str = "", **kwargs: Any) -> NoReturn: ...
