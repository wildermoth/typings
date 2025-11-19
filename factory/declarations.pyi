"""
Type stubs for factory.declarations module.

All declaration classes for defining factory attributes.
"""

from typing import Any, Callable, Dict, Iterable, Iterator as IteratorType, NamedTuple, Type, TypeVar, overload
from . import builder, enums, utils

_T = TypeVar('_T')
_M = TypeVar('_M')

class BaseDeclaration(utils.OrderedBase):
    """
    Base class for all factory declarations.

    Declarations mark attributes as needing lazy evaluation, allowing them
    to reference other attributes in the same factory.
    """
    FACTORY_BUILDER_PHASE: str  # enums.BuilderPhase.ATTRIBUTE_RESOLUTION
    CAPTURE_OVERRIDES: bool  # Whether this declaration captures call-time overrides
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool  # Whether to unroll context before evaluation

    _defaults: Dict[str, Any]

    def __init__(self, **defaults: Any) -> None: ...

    def unroll_context(
        self,
        instance: Any,
        step: builder.BuildStep,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Unroll any nested declarations in the context."""
        ...

    def _unwrap_evaluate_pre(
        self,
        wrapped: Any,
        *,
        instance: Any,
        step: builder.BuildStep,
        overrides: Dict[str, Any]
    ) -> Any:
        """Evaluate a wrapped declaration (for Maybe, Transformer, etc.)."""
        ...

    def evaluate_pre(
        self,
        instance: Any,
        step: builder.BuildStep,
        overrides: Dict[str, Any]
    ) -> Any:
        """
        Evaluate this declaration before instantiation.

        Args:
            instance: The Resolver holding current attributes
            step: The current BuildStep
            overrides: Call-time overrides

        Returns:
            The computed value
        """
        ...

    def evaluate(
        self,
        instance: Any,
        step: builder.BuildStep,
        extra: Dict[str, Any]
    ) -> Any:
        """
        Evaluate this declaration.

        Args:
            instance: The Resolver holding current attributes
            step: The current BuildStep
            extra: Additional parameters

        Returns:
            The computed value
        """
        ...

# Compatibility alias
class OrderedDeclaration(BaseDeclaration):
    """Deprecated: Use BaseDeclaration instead."""
    ...

class LazyFunction(BaseDeclaration):
    """
    Call a function to generate a value.

    Example:
        created_at = factory.LazyFunction(datetime.now)
    """
    function: Callable[[], _T]

    def __init__(self, function: Callable[[], _T]) -> None: ...
    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> _T: ...

class LazyAttribute(BaseDeclaration):
    """
    Generate a value based on the object being built.

    Example:
        email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    """
    function: Callable[[Any], _T]

    def __init__(self, function: Callable[[Any], _T]) -> None: ...
    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> _T: ...

class Transformer(BaseDeclaration):
    """
    Transform a value (or declaration) with a function.

    The transformer can be bypassed using Transformer.Force().

    Example:
        password = factory.Transformer('default', transform=hash_password)
        # Can override with: UserFactory(password=Transformer.Force('plain'))
    """
    CAPTURE_OVERRIDES: bool  # True
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool  # False

    class Force:
        """Bypass the transformer's transformation."""
        forced_value: Any
        def __init__(self, forced_value: Any) -> None: ...
        def __repr__(self) -> str: ...

    default: Any
    transform: Callable[[Any], _T]

    def __init__(self, default: Any, *, transform: Callable[[Any], _T]) -> None: ...
    def evaluate_pre(
        self,
        instance: Any,
        step: builder.BuildStep,
        overrides: Dict[str, Any]
    ) -> _T: ...

class _UNSPECIFIED:
    """Sentinel for unspecified default values."""
    ...

def deepgetattr(obj: Any, name: str, default: Any = ...) -> Any:
    """
    Get an attribute from an object, supporting dot notation.

    Args:
        obj: The object to query
        name: Attribute name (may contain dots for nested access)
        default: Default value if attribute not found

    Returns:
        The attribute value

    Raises:
        AttributeError: If attribute not found and no default provided
    """
    ...

class SelfAttribute(BaseDeclaration):
    """
    Reference another attribute of the object being built.

    Supports dot notation for nested attributes. If the attribute name starts
    with dots, it references parent factories in SubFactory chains.

    Example:
        author_name = factory.SelfAttribute('author.username')
        parent_id = factory.SelfAttribute('..id')  # From parent factory
    """
    depth: int
    attribute_name: str
    default: Any

    @overload
    def __init__(self, attribute_name: str) -> None: ...

    @overload
    def __init__(self, attribute_name: str, default: _T) -> None: ...

    def __init__(self, attribute_name: str, default: Any = ...) -> None: ...

    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> Any: ...
    def __repr__(self) -> str: ...

class Iterator(BaseDeclaration):
    """
    Cycle through an iterable.

    Example:
        status = factory.Iterator(['pending', 'active', 'closed'])
        user = factory.Iterator(User.objects.all())
    """
    getter: Callable[[Any], _T] | None
    iterator: utils.ResetableIterator[_T] | None
    iterator_builder: Callable[[], utils.ResetableIterator[_T]]

    @overload
    def __init__(
        self,
        iterator: Iterable[_T],
        cycle: bool = True
    ) -> None: ...

    @overload
    def __init__(
        self,
        iterator: Iterable[_M],
        cycle: bool = True,
        getter: Callable[[_M], _T] = ...
    ) -> None: ...

    def __init__(
        self,
        iterator: Iterable[Any],
        cycle: bool = True,
        getter: Callable[[Any], Any] | None = None
    ) -> None: ...

    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> _T: ...

    def reset(self) -> None:
        """Reset the iterator to its starting point."""
        ...

class Sequence(BaseDeclaration):
    """
    Generate sequential values.

    Example:
        username = factory.Sequence(lambda n: f'user{n}')
    """
    function: Callable[[int], _T]

    def __init__(self, function: Callable[[int], _T]) -> None: ...
    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> _T: ...

class LazyAttributeSequence(Sequence):
    """
    Combine LazyAttribute and Sequence.

    Example:
        username = factory.LazyAttributeSequence(
            lambda obj, n: f'{obj.first_name.lower()}{n}'
        )
    """
    function: Callable[[Any, int], _T]

    def __init__(self, function: Callable[[Any, int], _T]) -> None: ...
    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> _T: ...

class ContainerAttribute(BaseDeclaration):
    """
    Access the parent factory chain in SubFactory contexts.

    Example:
        # In a subfactory:
        parent_ref = factory.ContainerAttribute(
            lambda obj, containers: containers[0].id
        )
    """
    function: Callable[[Any, tuple[Any, ...]], _T]
    strict: bool

    def __init__(
        self,
        function: Callable[[Any, tuple[Any, ...]], _T],
        strict: bool = True
    ) -> None: ...

    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> _T: ...

class ParameteredAttribute(BaseDeclaration):
    """
    Base class for attributes that accept parameters.

    Subclasses must implement the generate() method.
    """
    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> Any: ...
    def generate(self, step: builder.BuildStep, params: Dict[str, Any]) -> Any:
        """Generate the attribute value."""
        ...

class _FactoryWrapper:
    """
    Handle factory arguments that can be either a class or an import path.

    Example:
        'myapp.factories.UserFactory' or UserFactory
    """
    factory: Type[Any] | None
    module: str
    name: str

    def __init__(self, factory_or_path: Type[Any] | str) -> None: ...
    def get(self) -> Type[Any]:
        """Get the factory class, importing if necessary."""
        ...
    def __repr__(self) -> str: ...

class SubFactory(BaseDeclaration):
    """
    Define a relationship to another factory.

    Example:
        author = factory.SubFactory(UserFactory)
        author = factory.SubFactory(UserFactory, username='admin')
        author = factory.SubFactory('myapp.factories.UserFactory')
    """
    FORCE_SEQUENCE: bool  # False
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool  # False

    factory_wrapper: _FactoryWrapper

    def __init__(
        self,
        factory: Type[Any] | str,
        **kwargs: Any
    ) -> None: ...

    def get_factory(self) -> Type[Any]:
        """Get the wrapped factory class."""
        ...

    def evaluate(self, instance: Any, step: builder.BuildStep, extra: Dict[str, Any]) -> Any: ...

class Dict(SubFactory):
    """
    Generate a dictionary with declarations as values.

    Example:
        metadata = factory.Dict({
            'created': factory.LazyFunction(datetime.now),
            'count': factory.Sequence(lambda n: n),
        })
    """
    FORCE_SEQUENCE: bool  # True

    def __init__(
        self,
        params: Dict[str, Any],
        dict_factory: str = 'factory.DictFactory'
    ) -> None: ...

class List(SubFactory):
    """
    Generate a list with declarations as elements.

    Example:
        tags = factory.List([
            'default',
            factory.Sequence(lambda n: f'tag-{n}'),
        ])
    """
    FORCE_SEQUENCE: bool  # True

    def __init__(
        self,
        params: list[Any],
        list_factory: str = 'factory.ListFactory'
    ) -> None: ...

class Skip:
    """Sentinel value for skipping an attribute."""
    def __bool__(self) -> bool: ...

# Global SKIP sentinel
SKIP: Skip

class Maybe(BaseDeclaration):
    """
    Conditionally use one of two declarations based on a parameter.

    Example:
        class UserFactory(factory.Factory):
            class Meta:
                model = User

            is_staff = factory.Trait(
                role='staff',
                permissions=factory.Maybe(
                    'is_staff',
                    yes_declaration=['admin', 'write', 'read'],
                    no_declaration=['read'],
                )
            )
    """
    decider: BaseDeclaration
    yes: Any
    no: Any
    FACTORY_BUILDER_PHASE: str

    def __init__(
        self,
        decider: str | BaseDeclaration,
        yes_declaration: Any = SKIP,
        no_declaration: Any = SKIP
    ) -> None: ...

    def evaluate_post(
        self,
        instance: Any,
        step: builder.BuildStep,
        overrides: Dict[str, Any]
    ) -> Any: ...

    def evaluate_pre(
        self,
        instance: Any,
        step: builder.BuildStep,
        overrides: Dict[str, Any]
    ) -> Any: ...

    def __repr__(self) -> str: ...

class Parameter(utils.OrderedBase):
    """
    Define a parameter that doesn't appear on the generated object.

    Used in the factory's Params class to control behavior without
    setting attributes on the model.

    Example:
        class UserFactory(factory.Factory):
            class Meta:
                model = User

            is_admin = factory.Parameter(False)
            role = factory.Maybe('is_admin',
                yes_declaration='admin',
                no_declaration='user'
            )
    """
    def as_declarations(
        self,
        field_name: str,
        declarations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compute declaration overrides for this parameter.

        Args:
            field_name: The parameter name
            declarations: Global factory declarations

        Returns:
            Dict of declarations to override
        """
        ...

    def get_revdeps(self, parameters: Dict[str, Parameter]) -> list[str]:
        """Get list of other parameters this one modifies."""
        ...

class SimpleParameter(Parameter):
    """Simple parameter with a fixed default value."""
    value: Any

    def __init__(self, value: Any) -> None: ...

    def as_declarations(
        self,
        field_name: str,
        declarations: Dict[str, Any]
    ) -> Dict[str, Any]: ...

    @classmethod
    def wrap(cls, value: Any) -> Parameter:
        """Wrap a value as a Parameter if it isn't already."""
        ...

class Trait(Parameter):
    """
    Named set of attribute overrides activated by a boolean parameter.

    Example:
        class UserFactory(factory.Factory):
            class Meta:
                model = User

            username = 'user'
            role = 'user'

            class Params:
                admin = factory.Trait(
                    username='admin',
                    role='administrator',
                )

        # Usage:
        regular_user = UserFactory()  # role='user'
        admin_user = UserFactory(admin=True)  # role='administrator'
    """
    overrides: Dict[str, Any]

    def __init__(self, **overrides: Any) -> None: ...

    def as_declarations(
        self,
        field_name: str,
        declarations: Dict[str, Any]
    ) -> Dict[str, Any]: ...

    def get_revdeps(self, parameters: Dict[str, Parameter]) -> list[str]: ...
    def __repr__(self) -> str: ...

# Post-generation declarations

class PostGenerationContext(NamedTuple):
    """Context passed to post-generation hooks."""
    value_provided: bool  # Whether a value was explicitly provided
    value: Any  # The provided value (or None)
    extra: Dict[str, Any]  # Extra keyword arguments

class PostGenerationDeclaration(BaseDeclaration):
    """
    Base class for declarations called after object instantiation.

    These are used for operations that need the created object,
    such as setting many-to-many relationships.
    """
    FACTORY_BUILDER_PHASE: str  # enums.BuilderPhase.POST_INSTANTIATION

    def evaluate_post(
        self,
        instance: Any,
        step: builder.BuildStep,
        overrides: Dict[str, Any]
    ) -> Any:
        """Evaluate the post-generation hook."""
        ...

    def call(
        self,
        instance: Any,
        step: builder.BuildStep,
        context: PostGenerationContext
    ) -> Any:
        """
        Execute the post-generation hook.

        Args:
            instance: The generated object
            step: The build step
            context: Post-generation context with value and extras

        Returns:
            Optional return value
        """
        ...

class PostGeneration(PostGenerationDeclaration):
    """
    Call a function after object generation.

    Example:
        @factory.post_generation
        def set_password(obj, create, extracted, **kwargs):
            if extracted:
                obj.set_password(extracted)
            elif create:
                obj.set_password('default')
    """
    function: Callable[[Any, bool, Any], Any]

    def __init__(self, function: Callable[[Any, bool, Any], Any]) -> None: ...

    def call(
        self,
        instance: Any,
        step: builder.BuildStep,
        context: PostGenerationContext
    ) -> Any: ...

class RelatedFactory(PostGenerationDeclaration):
    """
    Create related objects after generating the main object.

    Example:
        class UserFactory(factory.Factory):
            class Meta:
                model = User

        class PostFactory(factory.Factory):
            class Meta:
                model = Post
            author = factory.SubFactory(UserFactory)

        class UserWithPostsFactory(UserFactory):
            post = factory.RelatedFactory(PostFactory, 'author')
    """
    UNROLL_CONTEXT_BEFORE_EVALUATION: bool  # False

    name: str
    defaults: Dict[str, Any]
    factory_wrapper: _FactoryWrapper

    def __init__(
        self,
        factory: Type[Any] | str,
        factory_related_name: str = '',
        **defaults: Any
    ) -> None: ...

    def get_factory(self) -> Type[Any]:
        """Get the wrapped factory class."""
        ...

    def call(
        self,
        instance: Any,
        step: builder.BuildStep,
        context: PostGenerationContext
    ) -> Any: ...

class RelatedFactoryList(RelatedFactory):
    """
    Create multiple related objects.

    Example:
        class UserFactory(factory.Factory):
            posts = factory.RelatedFactoryList(
                PostFactory,
                'author',
                size=5,
            )
    """
    size: int | Callable[[], int]

    def __init__(
        self,
        factory: Type[Any] | str,
        factory_related_name: str = '',
        size: int | Callable[[], int] = 2,
        **defaults: Any
    ) -> None: ...

    def call(
        self,
        instance: Any,
        step: builder.BuildStep,
        context: PostGenerationContext
    ) -> list[Any]: ...

class NotProvided:
    """Sentinel for PostGenerationMethodCall when no value is provided."""
    ...

class PostGenerationMethodCall(PostGenerationDeclaration):
    """
    Call a method on the generated object.

    Example:
        class UserFactory(factory.Factory):
            class Meta:
                model = User

            password = factory.PostGenerationMethodCall('set_password', 'default123')

        # Usage:
        user = UserFactory()  # calls user.set_password('default123')
        user = UserFactory(password='custom')  # calls user.set_password('custom')
    """
    method_name: str
    method_arg: Any
    method_kwargs: Dict[str, Any]

    def __init__(
        self,
        method_name: str,
        *args: Any,
        **kwargs: Any
    ) -> None: ...

    def call(
        self,
        instance: Any,
        step: builder.BuildStep,
        context: PostGenerationContext
    ) -> Any: ...
