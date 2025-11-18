from typing import Any, Optional

class Client:
    def __init__(self, credentials: Any = ..., project: Optional[str] = ..., client_info: Any = ..., client_options: Any = ...) -> None: ...

class ClientWithProject(Client):
    project: str
    def __init__(self, project: Optional[str] = ..., credentials: Any = ..., client_info: Any = ..., client_options: Any = ...) -> None: ...
