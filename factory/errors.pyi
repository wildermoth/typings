"""
Type stubs for factory.errors module.

Exception classes used throughout factory_boy.
"""

class FactoryError(Exception):
    """Base exception for any factory_boy error."""
    ...

class AssociatedClassError(FactoryError):
    """Exception raised when a Factory subclass has no Meta.model set."""
    ...

class UnknownStrategy(FactoryError):
    """Exception raised when a factory uses an unknown build strategy."""
    ...

class UnsupportedStrategy(FactoryError):
    """Exception raised when trying to use a strategy incompatible with a Factory."""
    ...

class CyclicDefinitionError(FactoryError):
    """Exception raised when a cyclical declaration dependency is detected."""
    ...

class InvalidDeclarationError(FactoryError):
    """
    Exception raised when a declaration is invalid.

    This typically occurs when a sub-declaration (e.g., 'foo__bar') is defined
    without a corresponding parent declaration ('foo').
    """
    ...
