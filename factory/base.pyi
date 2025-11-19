"""
Type stubs for factory.base module.

Core Factory classes and metaclasses.
"""

from typing import Any, Callable, ClassVar, Dict, Generic, List as ListType, Sequence, Type, TypeVar, overload
from . import builder, declarations, errors

_T = TypeVar('_T')
_FactoryT = TypeVar('_FactoryT', bound='BaseFactory[Any]')

def get_factory_bases(bases: tuple[type, ...]) -> list[type]:
    """Retrieve all FactoryMetaClass-derived bases from a list."""
    ...

def resolve_attribute(
    name: str,
    bases: Sequence[type],
    default: Any = None
) -> Any:
    """Find the first definition of an attribute in MRO order."""
    ...

class FactoryMetaClass(type):
    """
    Metaclass for Factory classes.

    Handles collection and registration of factory declarations,
    and provides the syntax Factory() -> Factory.create() or Factory.build().
    """
    _meta: FactoryOptions

    def __call__(cls, **kwargs: Any) -> Any:
        """
        Override Factory() to call the default strategy.

        Returns an instance of the associated model class.
        """
        ...

    def __new__(
        mcs,
        class_name: str,
        bases: tuple[type, ...],
        attrs: Dict[str, Any]
    ) -> FactoryMetaClass: ...

    def __str__(cls) -> str: ...

class BaseMeta:
    """Default values for Factory.Meta attributes."""
    abstract: bool  # True
    strategy: str  # enums.CREATE_STRATEGY

class OptionDefault:
    """
    Default value specification for a Factory.Meta option.

    Attributes:
        name: The option name
        value: The default value
        inherit: Whether to inherit from parent factory's Meta
        checker: Optional validation function
    """
    name: str
    value: Any
    inherit: bool
    checker: Callable[[Any, Any], None] | None

    def __init__(
        self,
        name: str,
        value: Any,
        inherit: bool = False,
        checker: Callable[[Any, Any], None] | None = None
    ) -> None: ...

    def apply(self, meta: Any, base_meta: FactoryOptions | None) -> Any:
        """
        Compute the final value for this option.

        Args:
            meta: The factory's Meta class
            base_meta: The parent factory's _meta

        Returns:
            The computed value
        """
        ...

    def __str__(self) -> str: ...

class FactoryOptions:
    """
    Configuration options for a Factory.

    Attributes:
        factory: The factory class this belongs to
        base_factory: The parent factory class
        base_declarations: Declarations defined on this factory
        parameters: Params defined on this factory
        parameters_dependencies: Dependencies between parameters
        pre_declarations: Pre-instantiation declarations
        post_declarations: Post-instantiation declarations
        model: The model class to instantiate
        abstract: Whether this is an abstract factory
        strategy: The default build strategy
        inline_args: Arguments to pass inline to model constructor
        exclude: Field names to exclude from instantiation
        rename: Mapping of factory field names to model field names
    """
    factory: Type[BaseFactory[Any]] | None
    base_factory: Type[BaseFactory[Any]] | None
    base_declarations: Dict[str, Any]
    parameters: Dict[str, declarations.Parameter]
    parameters_dependencies: Dict[str, set[str]]
    pre_declarations: builder.DeclarationSet
    post_declarations: builder.DeclarationSet

    # Options from Meta
    model: Type[Any] | None
    abstract: bool
    strategy: str
    inline_args: Sequence[str]
    exclude: Sequence[str]
    rename: Dict[str, str]

    # Sequence counter
    _counter: _Counter | None
    counter_reference: FactoryOptions | None

    def __init__(self) -> None: ...

    @property
    def declarations(self) -> Dict[str, Any]:
        """Get all declarations including those from parameters."""
        ...

    def _build_default_options(self) -> list[OptionDefault]:
        """
        Provide default values for all allowed Meta options.

        Subclasses should extend this list for custom options.

        Returns:
            List of OptionDefault instances
        """
        ...

    def _fill_from_meta(
        self,
        meta: Any,
        base_meta: FactoryOptions | None
    ) -> None:
        """Fill options from the factory's Meta class."""
        ...

    def contribute_to_class(
        self,
        factory: Type[BaseFactory[Any]],
        meta: Any = None,
        base_meta: FactoryOptions | None = None,
        base_factory: Type[BaseFactory[Any]] | None = None,
        params: Any = None
    ) -> None:
        """
        Attach this options instance to a factory class.

        Args:
            factory: The factory class
            meta: The factory's Meta class
            base_meta: The parent factory's _meta
            base_factory: The parent factory class
            params: The factory's Params class
        """
        ...

    def _get_counter_reference(self) -> FactoryOptions:
        """Identify which factory should manage the shared sequence counter."""
        ...

    def _initialize_counter(self) -> None:
        """Initialize the sequence counter (lazy initialization)."""
        ...

    def next_sequence(self) -> int:
        """
        Get the next sequence number.

        Returns:
            The next sequence number
        """
        ...

    def reset_sequence(self, value: int | None = None, force: bool = False) -> None:
        """
        Reset the sequence counter.

        Args:
            value: The value to reset to (or None to call _setup_next_sequence)
            force: Whether to force reset on descendant factories
        """
        ...

    def prepare_arguments(self, attributes: Dict[str, Any]) -> tuple[tuple[Any, ...], Dict[str, Any]]:
        """
        Convert attributes dict to (args, kwargs) for model instantiation.

        Args:
            attributes: The computed attributes

        Returns:
            Tuple of (args, kwargs)
        """
        ...

    def instantiate(
        self,
        step: builder.BuildStep,
        args: tuple[Any, ...],
        kwargs: Dict[str, Any]
    ) -> Any:
        """
        Create the model instance.

        Args:
            step: The build step
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            The created instance
        """
        ...

    def use_postgeneration_results(
        self,
        step: builder.BuildStep,
        instance: Any,
        results: Dict[str, Any]
    ) -> None:
        """
        Handle post-generation results.

        Args:
            step: The build step
            instance: The created instance
            results: Results from post-generation hooks
        """
        ...

    def _is_declaration(self, name: str, value: Any) -> bool:
        """
        Check if a class attribute is a declaration.

        Args:
            name: The attribute name
            value: The attribute value

        Returns:
            True if it's a declaration
        """
        ...

    def _check_parameter_dependencies(
        self,
        parameters: Dict[str, declarations.Parameter]
    ) -> Dict[str, set[str]]:
        """
        Check for cyclical parameter dependencies.

        Args:
            parameters: The parameters to check

        Returns:
            Dict of dependencies

        Raises:
            CyclicDefinitionError: If cycles are detected
        """
        ...

    def get_model_class(self) -> Type[Any] | None:
        """
        Get the model class to instantiate.

        Extension point for ORM-specific factories to resolve model references.

        Returns:
            The model class or None
        """
        ...

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class _Counter:
    """Simple sequence counter."""
    seq: int

    def __init__(self, seq: int) -> None: ...

    def next(self) -> int:
        """Get the next sequence value and increment."""
        ...

    def reset(self, next_value: int = 0) -> None:
        """Reset the counter to a specific value."""
        ...

class BaseFactory(Generic[_T]):
    """
    Base factory class with sequence support and build strategies.

    Type parameter _T represents the type of object this factory creates.

    Example:
        class UserFactory(factory.Factory):
            class Meta:
                model = User

            username = factory.Sequence(lambda n: f'user{n}')
            email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

        # Usage:
        user = UserFactory()  # Uses default strategy (create)
        user = UserFactory.build()  # Build without saving
        user = UserFactory.create()  # Create and save
        users = UserFactory.create_batch(5)  # Create 5 instances
    """

    # Backwards compatibility
    UnknownStrategy: Type[errors.UnknownStrategy]
    UnsupportedStrategy: Type[errors.UnsupportedStrategy]

    _meta: ClassVar[FactoryOptions]
    _options_class: ClassVar[Type[FactoryOptions]]

    def __new__(cls, *args: Any, **kwargs: Any) -> None:
        """Prevent direct instantiation of factories."""
        ...

    @classmethod
    def reset_sequence(cls, value: int | None = None, force: bool = False) -> None:
        """
        Reset the sequence counter.

        Args:
            value: The value to reset to (or None to recompute)
            force: Whether to force reset on parent factories
        """
        ...

    @classmethod
    def _setup_next_sequence(cls) -> int:
        """
        Determine the initial sequence value.

        Override to customize sequence initialization (e.g., from database).

        Returns:
            The initial sequence value (default: 0)
        """
        ...

    @classmethod
    def _adjust_kwargs(cls, **kwargs: Any) -> Dict[str, Any]:
        """
        Extension point for adjusting kwargs before building.

        Args:
            **kwargs: The kwargs to adjust

        Returns:
            Adjusted kwargs
        """
        ...

    @classmethod
    def _generate(cls, strategy: str, params: Dict[str, Any]) -> _T:
        """
        Generate an object using the specified strategy.

        Args:
            strategy: The build strategy
            params: Attribute overrides

        Returns:
            The generated instance
        """
        ...

    @classmethod
    def _after_postgeneration(
        cls,
        instance: _T,
        create: bool,
        results: Dict[str, Any] | None = None
    ) -> None:
        """
        Hook called after post-generation declarations.

        Args:
            instance: The generated object
            create: Whether this was a 'create' operation
            results: Results from post-generation hooks
        """
        ...

    @classmethod
    def _build(cls, model_class: Type[_T], *args: Any, **kwargs: Any) -> _T:
        """
        Build an instance of the model class.

        Override to customize instantiation logic.

        Args:
            model_class: The class to instantiate
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            The built instance
        """
        ...

    @classmethod
    def _create(cls, model_class: Type[_T], *args: Any, **kwargs: Any) -> _T:
        """
        Create and save an instance of the model class.

        Override to customize creation/persistence logic.

        Args:
            model_class: The class to instantiate
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            The created instance
        """
        ...

    @classmethod
    def build(cls, **kwargs: Any) -> _T:
        """
        Build an instance without persisting to any datastore.

        Args:
            **kwargs: Attribute overrides

        Returns:
            The built instance
        """
        ...

    @classmethod
    def build_batch(cls, size: int, **kwargs: Any) -> ListType[_T]:
        """
        Build a batch of instances without persisting.

        Args:
            size: Number of instances to build
            **kwargs: Attribute overrides

        Returns:
            List of built instances
        """
        ...

    @classmethod
    def create(cls, **kwargs: Any) -> _T:
        """
        Create and persist an instance to the datastore.

        Args:
            **kwargs: Attribute overrides

        Returns:
            The created instance
        """
        ...

    @classmethod
    def create_batch(cls, size: int, **kwargs: Any) -> ListType[_T]:
        """
        Create and persist a batch of instances.

        Args:
            size: Number of instances to create
            **kwargs: Attribute overrides

        Returns:
            List of created instances
        """
        ...

    @classmethod
    def stub(cls, **kwargs: Any) -> Any:
        """
        Create a stub object with the specified attributes.

        Stub objects have attributes but no specific class.

        Args:
            **kwargs: Attribute overrides

        Returns:
            A stub object
        """
        ...

    @classmethod
    def stub_batch(cls, size: int, **kwargs: Any) -> ListType[Any]:
        """
        Create a batch of stub objects.

        Args:
            size: Number of stubs to create
            **kwargs: Attribute overrides

        Returns:
            List of stub objects
        """
        ...

    @classmethod
    def generate(cls, strategy: str, **kwargs: Any) -> _T | Any:
        """
        Generate an instance using the specified strategy.

        Args:
            strategy: The strategy (BUILD_STRATEGY, CREATE_STRATEGY, or STUB_STRATEGY)
            **kwargs: Attribute overrides

        Returns:
            The generated instance
        """
        ...

    @classmethod
    def generate_batch(cls, strategy: str, size: int, **kwargs: Any) -> ListType[_T | Any]:
        """
        Generate a batch using the specified strategy.

        Args:
            strategy: The strategy
            size: Number of instances to generate
            **kwargs: Attribute overrides

        Returns:
            List of generated instances
        """
        ...

    @classmethod
    def simple_generate(cls, create: bool, **kwargs: Any) -> _T:
        """
        Generate an instance using a simple create/build choice.

        Args:
            create: If True, use CREATE_STRATEGY; otherwise BUILD_STRATEGY
            **kwargs: Attribute overrides

        Returns:
            The generated instance
        """
        ...

    @classmethod
    def simple_generate_batch(cls, create: bool, size: int, **kwargs: Any) -> ListType[_T]:
        """
        Generate a batch using a simple create/build choice.

        Args:
            create: If True, use CREATE_STRATEGY; otherwise BUILD_STRATEGY
            size: Number of instances to generate
            **kwargs: Attribute overrides

        Returns:
            List of generated instances
        """
        ...

class Factory(BaseFactory[_T], metaclass=FactoryMetaClass):
    """
    Main factory class for creating model instances.

    Example:
        class UserFactory(factory.Factory):
            class Meta:
                model = User

            username = factory.Sequence(lambda n: f'user{n}')
    """
    AssociatedClassError: Type[errors.AssociatedClassError]

    class Meta(BaseMeta):
        """Meta configuration for the factory."""
        ...

class StubObject:
    """A generic container for stub objects."""
    def __init__(self, **kwargs: Any) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class StubFactory(Factory[StubObject]):
    """
    Factory that creates stub objects instead of model instances.

    Stub objects have attributes but no specific class.
    """
    class Meta:
        model: Type[StubObject]
        strategy: str  # STUB_STRATEGY

    @classmethod
    def build(cls, **kwargs: Any) -> StubObject: ...

    @classmethod
    def create(cls, **kwargs: Any) -> StubObject: ...

class BaseDictFactory(Factory[Dict[str, Any]]):
    """Abstract factory for dictionary-like classes."""
    class Meta:
        abstract: bool  # True

    @classmethod
    def _build(cls, model_class: Type[_T], *args: Any, **kwargs: Any) -> _T: ...

    @classmethod
    def _create(cls, model_class: Type[_T], *args: Any, **kwargs: Any) -> _T: ...

class DictFactory(BaseDictFactory):
    """Factory for creating dict instances."""
    class Meta:
        model: Type[dict]

class BaseListFactory(Factory[ListType[Any]]):
    """Abstract factory for list-like classes."""
    class Meta:
        abstract: bool  # True

    @classmethod
    def _build(cls, model_class: Type[_T], *args: Any, **kwargs: Any) -> _T: ...

    @classmethod
    def _create(cls, model_class: Type[_T], *args: Any, **kwargs: Any) -> _T: ...

class ListFactory(BaseListFactory):
    """Factory for creating list instances."""
    class Meta:
        model: Type[list]

def use_strategy(new_strategy: str) -> Callable[[Type[_FactoryT]], Type[_FactoryT]]:
    """
    Decorator to force a different default strategy.

    DEPRECATED: Set Meta.strategy instead.

    Args:
        new_strategy: The strategy to use

    Returns:
        Decorator function
    """
    ...
