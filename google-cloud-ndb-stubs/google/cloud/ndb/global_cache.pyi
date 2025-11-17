"""Type stubs for google.cloud.ndb.global_cache"""

from typing import Any, Dict, Iterable, List, Optional

from google.cloud.ndb import key as key_module

class GlobalCache:
    """Base class for global cache implementations."""

    def get(self, keys: Iterable[bytes]) -> List[Optional[bytes]]: ...
    def set(self, items: Dict[bytes, bytes], expires: Optional[float] = ...) -> None: ...
    def delete(self, keys: Iterable[bytes]) -> None: ...
    def watch(self, keys: Iterable[bytes]) -> None: ...
    def compare_and_swap(
        self,
        items: Dict[bytes, bytes],
        expires: Optional[float] = ...,
    ) -> None: ...
    def clear(self) -> None: ...

class MemcacheCache(GlobalCache):
    """Memcache-based global cache implementation."""

    def __init__(
        self,
        servers: Optional[List[str]] = ...,
        **options: Any,
    ) -> None: ...

class RedisCache(GlobalCache):
    """Redis-based global cache implementation."""

    def __init__(
        self,
        redis_client: Any,
        **options: Any,
    ) -> None: ...
