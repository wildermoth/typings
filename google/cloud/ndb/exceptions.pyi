"""Type stubs for google.cloud.ndb.exceptions"""

class Error(Exception):
    """Base exception for all NDB errors."""
    ...

class BadValueError(Error):
    """Raised when a property value is invalid."""
    ...

class BadRequestError(Error):
    """Raised when a bad request is made to the datastore."""
    ...

class BadArgumentError(Error):
    """Raised when an argument to a function is invalid."""
    ...

class BadQueryError(Error):
    """Raised when a query is invalid."""
    ...

class BadFilterError(BadQueryError):
    """Raised when a filter is invalid."""
    ...

class BadPropertyError(Error):
    """Raised when a property is accessed incorrectly."""
    ...

class BadKeyError(Error):
    """Raised when a key is malformed."""
    ...

class ContextError(Error):
    """Raised when a context operation fails."""
    ...

class NoLongerImplementedError(Error):
    """Raised when a feature is no longer supported."""
    ...

class Rollback(Exception):
    """Raised to explicitly roll back a transaction."""
    ...
