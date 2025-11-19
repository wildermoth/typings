"""
Type stubs for factory.builder module.

Build infrastructure for creating factory instances.
"""

from typing import Any, Dict, Iterable, Iterator, NamedTuple, Optional
from collections import defaultdict

from . import base

class DeclarationWithContext(NamedTuple):
    """A declaration along with its context (nested parameters)."""
    name: str
    declaration: Any
    context: Dict[str, Any]

class DeclarationSet:
    """
    A set of declarations with their nested parameters.

    Behaves like a dict mapping top-level declaration names to
    DeclarationWithContext instances.

    Attributes:
        declarations: Top-level declarations (name => declaration)
        contexts: Nested parameters for each declaration (name => {subfield => value})
    """
    declarations: Dict[str, Any]
    contexts: defaultdict[str, Dict[str, Any]]

    def __init__(self, initial: Dict[str, Any] | None = None) -> None: ...

    @classmethod
    def split(cls, entry: str) -> tuple[str, str | None]:
        """
        Split a declaration name into (root, subpath) components.

        Examples:
            >>> DeclarationSet.split('foo__bar')
            ('foo', 'bar')
            >>> DeclarationSet.split('foo')
            ('foo', None)
            >>> DeclarationSet.split('foo__bar__baz')
            ('foo', 'bar__baz')
        """
        ...

    @classmethod
    def join(cls, root: str, subkey: str | None) -> str:
        """
        Rebuild a full declaration name from its components.

        For every string x: join(split(x)) == x
        """
        ...

    def copy(self) -> DeclarationSet: ...

    def update(self, values: Dict[str, Any]) -> None:
        """
        Add new declarations to this set.

        Args:
            values: The declarations to add
        """
        ...

    def filter(self, entries: Iterable[str]) -> list[str]:
        """
        Filter a set of declaration names to those related to this set.

        Keeps declarations that override current ones or are parameters to them.
        """
        ...

    def sorted(self) -> list[str]:
        """Return declaration names sorted by creation order."""
        ...

    def __contains__(self, key: str) -> bool: ...
    def __getitem__(self, key: str) -> DeclarationWithContext: ...
    def __iter__(self) -> Iterator[str]: ...

    def values(self) -> Iterator[DeclarationWithContext]:
        """Iterate over declarations with their contexts."""
        ...

    def _items(self) -> Iterator[tuple[str, Any]]:
        """Extract (key, value) pairs suitable for __init__."""
        ...

    def as_dict(self) -> Dict[str, Any]:
        """Return a dict suitable for __init__."""
        ...

    def __repr__(self) -> str: ...

def parse_declarations(
    decls: Dict[str, Any],
    base_pre: DeclarationSet | None = None,
    base_post: DeclarationSet | None = None
) -> tuple[DeclarationSet, DeclarationSet]:
    """
    Parse declarations into pre- and post-instantiation sets.

    Args:
        decls: Declarations to parse
        base_pre: Base pre-instantiation declarations
        base_post: Base post-instantiation declarations

    Returns:
        Tuple of (pre_declarations, post_declarations)
    """
    ...

class BuildStep:
    """
    A single step in building a factory instance.

    Attributes:
        builder: The StepBuilder coordinating this build
        sequence: The sequence number for this instance
        attributes: Computed attributes for this instance
        parent_step: The parent BuildStep (for subfactories)
        stub: The Resolver for lazy attribute evaluation
    """
    builder: StepBuilder
    sequence: int
    attributes: Dict[str, Any]
    parent_step: BuildStep | None
    stub: Resolver | None

    def __init__(
        self,
        builder: StepBuilder,
        sequence: int,
        parent_step: BuildStep | None = None
    ) -> None: ...

    def resolve(self, declarations: DeclarationSet) -> None:
        """
        Resolve all declarations and store results in attributes.

        Args:
            declarations: The declarations to resolve
        """
        ...

    @property
    def chain(self) -> tuple[Resolver | None, ...]:
        """
        Get the chain of Resolvers from this step to the root.

        Used for SelfAttribute lookups with depth > 1.
        """
        ...

    def recurse(
        self,
        factory: type[base.BaseFactory[Any]],
        declarations: Dict[str, Any],
        force_sequence: int | None = None
    ) -> Any:
        """
        Recursively build a subfactory instance.

        Args:
            factory: The factory class to build
            declarations: Additional declarations/overrides
            force_sequence: Optional forced sequence number

        Returns:
            The built instance
        """
        ...

    def __repr__(self) -> str: ...

class StepBuilder:
    """
    Coordinates building a factory instance.

    Attributes:
        factory_meta: The FactoryOptions for this build
        strategy: The build strategy (BUILD_STRATEGY, CREATE_STRATEGY, STUB_STRATEGY)
        extras: Extra kwargs passed to the factory
        force_init_sequence: Forced sequence number from __sequence parameter
    """
    factory_meta: base.FactoryOptions
    strategy: str
    extras: Dict[str, Any]
    force_init_sequence: int | None

    def __init__(
        self,
        factory_meta: base.FactoryOptions,
        extras: Dict[str, Any],
        strategy: str
    ) -> None: ...

    def build(
        self,
        parent_step: BuildStep | None = None,
        force_sequence: int | None = None
    ) -> Any:
        """
        Build the factory instance.

        Args:
            parent_step: Parent step (for subfactories)
            force_sequence: Optional forced sequence number

        Returns:
            The built instance
        """
        ...

    def recurse(
        self,
        factory_meta: base.FactoryOptions,
        extras: Dict[str, Any]
    ) -> StepBuilder:
        """
        Create a builder for a subfactory.

        Args:
            factory_meta: The subfactory's FactoryOptions
            extras: Extra declarations for the subfactory

        Returns:
            A new StepBuilder for the subfactory
        """
        ...

    def __repr__(self) -> str: ...

class Resolver:
    """
    Lazily resolves factory attribute values.

    Attributes are computed on-demand when accessed. This allows attributes
    to reference other attributes defined in the same factory.

    Cyclic dependencies are detected and raise CyclicDefinitionError.
    """
    def __init__(
        self,
        declarations: DeclarationSet,
        step: BuildStep,
        sequence: int
    ) -> None: ...

    @property
    def factory_parent(self) -> Resolver | None:
        """Get the parent factory's Resolver (for SubFactory contexts)."""
        ...

    def __repr__(self) -> str: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
