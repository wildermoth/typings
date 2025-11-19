"""
Type stubs for factory.helpers module.

Helper functions for creating and using factories.
"""

from typing import Any, Callable, ContextManager, Type, TypeVar
from . import base, declarations

_T = TypeVar('_T')

def debug(logger: str = 'factory', stream: Any = None) -> ContextManager[None]:
    """
    Context manager to enable debug logging for factories.

    Example:
        with factory.debug():
            user = UserFactory()
            # Logs all factory operations

    Args:
        logger: Logger name to use (default: 'factory')
        stream: Optional stream for the handler

    Returns:
        Context manager
    """
    ...

def make_factory(
    klass: Type[_T],
    **kwargs: Any
) -> Type[base.Factory[_T]]:
    """
    Dynamically create a factory for a given class.

    Example:
        UserFactory = factory.make_factory(
            User,
            username=factory.Sequence(lambda n: f'user{n}'),
            email=factory.LazyAttribute(lambda obj: f'{obj.username}@example.com'),
        )

    Args:
        klass: The model class
        **kwargs: Factory attributes (can include Meta, Params, or declarations)
        FACTORY_CLASS: Optional base factory class (default: Factory)

    Returns:
        A Factory subclass for the given model
    """
    ...

def build(klass: Type[_T], **kwargs: Any) -> _T:
    """
    Create a factory for the class and build an instance.

    Example:
        user = factory.build(User, username='alice')

    Args:
        klass: The model class
        **kwargs: Attributes for the factory

    Returns:
        A built instance
    """
    ...

def build_batch(klass: Type[_T], size: int, **kwargs: Any) -> list[_T]:
    """
    Create a factory for the class and build a batch of instances.

    Example:
        users = factory.build_batch(User, 5, is_active=True)

    Args:
        klass: The model class
        size: Number of instances to build
        **kwargs: Attributes for the factory

    Returns:
        List of built instances
    """
    ...

def create(klass: Type[_T], **kwargs: Any) -> _T:
    """
    Create a factory for the class and create an instance.

    Example:
        user = factory.create(User, username='alice')

    Args:
        klass: The model class
        **kwargs: Attributes for the factory

    Returns:
        A created instance
    """
    ...

def create_batch(klass: Type[_T], size: int, **kwargs: Any) -> list[_T]:
    """
    Create a factory for the class and create a batch of instances.

    Example:
        users = factory.create_batch(User, 5, is_active=True)

    Args:
        klass: The model class
        size: Number of instances to create
        **kwargs: Attributes for the factory

    Returns:
        List of created instances
    """
    ...

def stub(klass: Type[_T], **kwargs: Any) -> Any:
    """
    Create a factory for the class and stub an instance.

    Example:
        user_stub = factory.stub(User, username='alice')

    Args:
        klass: The model class
        **kwargs: Attributes for the factory

    Returns:
        A stub object
    """
    ...

def stub_batch(klass: Type[_T], size: int, **kwargs: Any) -> list[Any]:
    """
    Create a factory for the class and stub a batch of instances.

    Example:
        user_stubs = factory.stub_batch(User, 5)

    Args:
        klass: The model class
        size: Number of stubs to create
        **kwargs: Attributes for the factory

    Returns:
        List of stub objects
    """
    ...

def generate(klass: Type[_T], strategy: str, **kwargs: Any) -> _T | Any:
    """
    Create a factory for the class and generate an instance.

    Example:
        user = factory.generate(User, factory.CREATE_STRATEGY, username='alice')

    Args:
        klass: The model class
        strategy: The build strategy
        **kwargs: Attributes for the factory

    Returns:
        A generated instance
    """
    ...

def generate_batch(
    klass: Type[_T],
    strategy: str,
    size: int,
    **kwargs: Any
) -> list[_T | Any]:
    """
    Create a factory for the class and generate a batch.

    Example:
        users = factory.generate_batch(User, factory.BUILD_STRATEGY, 5)

    Args:
        klass: The model class
        strategy: The build strategy
        size: Number of instances to generate
        **kwargs: Attributes for the factory

    Returns:
        List of generated instances
    """
    ...

def simple_generate(klass: Type[_T], create: bool, **kwargs: Any) -> _T:
    """
    Create a factory for the class and simple_generate an instance.

    Example:
        user = factory.simple_generate(User, create=True, username='alice')

    Args:
        klass: The model class
        create: If True, create; otherwise build
        **kwargs: Attributes for the factory

    Returns:
        A generated instance
    """
    ...

def simple_generate_batch(
    klass: Type[_T],
    create: bool,
    size: int,
    **kwargs: Any
) -> list[_T]:
    """
    Create a factory for the class and simple_generate a batch.

    Example:
        users = factory.simple_generate_batch(User, create=False, size=5)

    Args:
        klass: The model class
        create: If True, create; otherwise build
        size: Number of instances to generate
        **kwargs: Attributes for the factory

    Returns:
        List of generated instances
    """
    ...

# Decorator helpers

def lazy_attribute(func: Callable[[Any], _T]) -> declarations.LazyAttribute:
    """
    Decorator form of LazyAttribute.

    Example:
        @factory.lazy_attribute
        def email(obj):
            return f'{obj.username}@example.com'

    Args:
        func: Function taking the object being built

    Returns:
        LazyAttribute declaration
    """
    ...

def iterator(func: Callable[[], Any]) -> declarations.Iterator:
    """
    Decorator to turn a generator function into an Iterator.

    Example:
        @factory.iterator
        def usernames():
            yield 'alice'
            yield 'bob'
            yield 'charlie'

    Args:
        func: Generator function

    Returns:
        Iterator declaration
    """
    ...

def sequence(func: Callable[[int], _T]) -> declarations.Sequence:
    """
    Decorator form of Sequence.

    Example:
        @factory.sequence
        def username(n):
            return f'user{n}'

    Args:
        func: Function taking a sequence number

    Returns:
        Sequence declaration
    """
    ...

def lazy_attribute_sequence(
    func: Callable[[Any, int], _T]
) -> declarations.LazyAttributeSequence:
    """
    Decorator form of LazyAttributeSequence.

    Example:
        @factory.lazy_attribute_sequence
        def username(obj, n):
            return f'{obj.first_name.lower()}{n}'

    Args:
        func: Function taking the object and sequence number

    Returns:
        LazyAttributeSequence declaration
    """
    ...

def container_attribute(
    func: Callable[[Any, tuple[Any, ...]], _T]
) -> declarations.ContainerAttribute:
    """
    Decorator form of ContainerAttribute (non-strict mode).

    Example:
        @factory.container_attribute
        def parent_id(obj, containers):
            if containers:
                return containers[0].id
            return None

    Args:
        func: Function taking the object and container chain

    Returns:
        ContainerAttribute declaration (strict=False)
    """
    ...

def post_generation(
    fun: Callable[[Any, bool, Any], None]
) -> declarations.PostGeneration:
    """
    Decorator form of PostGeneration.

    Example:
        @factory.post_generation
        def set_password(obj, create, extracted):
            if extracted:
                obj.set_password(extracted)

    Args:
        fun: Function taking (obj, create, extracted, **kwargs)

    Returns:
        PostGeneration declaration
    """
    ...
