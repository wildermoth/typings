"""Type stubs for google.cloud.ndb.client"""

from typing import Any, Optional

from google.auth.credentials import Credentials
from google.cloud.ndb import context as context_module

class Client:
    """Client for NDB operations.

    Use this client to create a context for NDB operations:
        client = ndb.Client(project='my-project')
        with client.context():
            # Perform NDB operations here
            entity.put()
    """

    SCOPE: tuple[str, ...]

    def __init__(
        self,
        project: Optional[str] = ...,
        namespace: Optional[str] = ...,
        credentials: Optional[Credentials] = ...,
        client_options: Optional[Any] = ...,
        client_info: Optional[Any] = ...,
        database: Optional[str] = ...,
    ) -> None: ...

    @property
    def project(self) -> str:
        """The project ID for this client."""
        ...

    @property
    def namespace(self) -> Optional[str]:
        """The namespace for this client."""
        ...

    @property
    def database(self) -> Optional[str]:
        """The database ID for this client."""
        ...

    def context(
        self,
        cache_policy: Optional[Any] = ...,
        global_cache: Optional[Any] = ...,
        global_cache_policy: Optional[Any] = ...,
        global_cache_timeout_policy: Optional[Any] = ...,
        legacy_data: bool = ...,
    ) -> context_module.Context:
        """Create a Context for NDB operations.

        Use as a context manager: with client.context(): ...
        """
        ...
