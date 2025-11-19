"""
Type stubs for factory_boy library.

Factory Boy is a fixtures replacement tool based on thoughtbot's factory_bot.
It provides a flexible and powerful way to create test data and fixtures.

Documentation: https://factoryboy.readthedocs.io/

Example:
    from factory import Factory, Sequence, LazyAttribute

    class UserFactory(Factory):
        class Meta:
            model = User

        username = Sequence(lambda n: f'user{n}')
        email = LazyAttribute(lambda obj: f'{obj.username}@example.com')

    # Usage:
    user = UserFactory()
    users = UserFactory.create_batch(5)
"""

from typing import Any, Callable, Type, TypeVar

# Core base classes
from .base import (
    Factory as Factory,
    StubFactory as StubFactory,
    FactoryOptions as FactoryOptions,
    BaseMeta as BaseMeta,
    OptionDefault as OptionDefault,
    BaseFactory as BaseFactory,
    DictFactory as DictFactory,
    ListFactory as ListFactory,
    BaseDictFactory as BaseDictFactory,
    BaseListFactory as BaseListFactory,
    use_strategy as use_strategy,
    StubObject as StubObject,
    FactoryMetaClass as FactoryMetaClass,
)

# Builder infrastructure
from .builder import (
    BuildStep as BuildStep,
    Resolver as Resolver,
    StepBuilder as StepBuilder,
    DeclarationSet as DeclarationSet,
    DeclarationWithContext as DeclarationWithContext,
)

# Core declarations
from .declarations import (
    OrderedDeclaration as OrderedDeclaration,
    BaseDeclaration as BaseDeclaration,
    LazyFunction as LazyFunction,
    LazyAttribute as LazyAttribute,
    LazyAttributeSequence as LazyAttributeSequence,
    Sequence as Sequence,
    SubFactory as SubFactory,
    Dict as Dict,
    List as List,
    Maybe as Maybe,
    SelfAttribute as SelfAttribute,
    Iterator as Iterator,
    Transformer as Transformer,
    # Container declarations
    ContainerAttribute as ContainerAttribute,
    ParameteredAttribute as ParameteredAttribute,
    # Post-generation
    PostGeneration as PostGeneration,
    PostGenerationMethodCall as PostGenerationMethodCall,
    RelatedFactory as RelatedFactory,
    RelatedFactoryList as RelatedFactoryList,
    PostGenerationDeclaration as PostGenerationDeclaration,
    PostGenerationContext as PostGenerationContext,
    # Parameters
    Parameter as Parameter,
    Trait as Trait,
    SimpleParameter as SimpleParameter,
    SKIP as SKIP,
)

# Faker integration
from .faker import (
    Faker as Faker,
)

# Fuzzy attributes
from .fuzzy import (
    BaseFuzzyAttribute as BaseFuzzyAttribute,
    FuzzyAttribute as FuzzyAttribute,
    FuzzyChoice as FuzzyChoice,
    FuzzyInteger as FuzzyInteger,
    FuzzyDecimal as FuzzyDecimal,
    FuzzyFloat as FuzzyFloat,
    FuzzyDate as FuzzyDate,
    FuzzyDateTime as FuzzyDateTime,
    FuzzyNaiveDateTime as FuzzyNaiveDateTime,
    FuzzyText as FuzzyText,
)

# Helper functions
from .helpers import (
    build as build,
    build_batch as build_batch,
    create as create,
    create_batch as create_batch,
    stub as stub,
    stub_batch as stub_batch,
    generate as generate,
    generate_batch as generate_batch,
    simple_generate as simple_generate,
    simple_generate_batch as simple_generate_batch,
    make_factory as make_factory,
    debug as debug,
    # Decorators
    lazy_attribute as lazy_attribute,
    lazy_attribute_sequence as lazy_attribute_sequence,
    sequence as sequence,
    iterator as iterator,
    container_attribute as container_attribute,
    post_generation as post_generation,
)

# Enums and constants
from .enums import (
    BUILD_STRATEGY as BUILD_STRATEGY,
    CREATE_STRATEGY as CREATE_STRATEGY,
    STUB_STRATEGY as STUB_STRATEGY,
    SPLITTER as SPLITTER,
    BuilderPhase as BuilderPhase,
)

# Errors
from .errors import (
    FactoryError as FactoryError,
    AssociatedClassError as AssociatedClassError,
    UnknownStrategy as UnknownStrategy,
    UnsupportedStrategy as UnsupportedStrategy,
    CyclicDefinitionError as CyclicDefinitionError,
    InvalidDeclarationError as InvalidDeclarationError,
)

# Utilities
from .utils import (
    OrderedBase as OrderedBase,
    ResetableIterator as ResetableIterator,
)

# Random state management
from .random import (
    get_random_state as get_random_state,
    set_random_state as set_random_state,
    reseed_random as reseed_random,
)

# Version info
__version__: str
__author__: str

# Type variables for convenience
_T = TypeVar('_T')
_FactoryT = TypeVar('_FactoryT', bound=Factory)

__all__ = [
    # Core classes
    'Factory',
    'StubFactory',
    'BaseFactory',
    'FactoryOptions',
    'BaseMeta',
    'OptionDefault',
    'DictFactory',
    'ListFactory',
    'BaseDictFactory',
    'BaseListFactory',
    'StubObject',
    'FactoryMetaClass',
    # Builder classes
    'BuildStep',
    'Resolver',
    'StepBuilder',
    'DeclarationSet',
    'DeclarationWithContext',
    # Declarations
    'OrderedDeclaration',
    'BaseDeclaration',
    'LazyFunction',
    'LazyAttribute',
    'LazyAttributeSequence',
    'Sequence',
    'SubFactory',
    'Dict',
    'List',
    'Maybe',
    'SelfAttribute',
    'Iterator',
    'Transformer',
    'ContainerAttribute',
    'ParameteredAttribute',
    # Post-generation
    'PostGeneration',
    'PostGenerationMethodCall',
    'RelatedFactory',
    'RelatedFactoryList',
    'PostGenerationDeclaration',
    'PostGenerationContext',
    # Parameters and Traits
    'Parameter',
    'Trait',
    'SimpleParameter',
    'SKIP',
    # Faker
    'Faker',
    # Fuzzy
    'BaseFuzzyAttribute',
    'FuzzyAttribute',
    'FuzzyChoice',
    'FuzzyInteger',
    'FuzzyDecimal',
    'FuzzyFloat',
    'FuzzyDate',
    'FuzzyDateTime',
    'FuzzyNaiveDateTime',
    'FuzzyText',
    # Helpers
    'build',
    'build_batch',
    'create',
    'create_batch',
    'stub',
    'stub_batch',
    'generate',
    'generate_batch',
    'simple_generate',
    'simple_generate_batch',
    'make_factory',
    'debug',
    'lazy_attribute',
    'lazy_attribute_sequence',
    'sequence',
    'iterator',
    'container_attribute',
    'post_generation',
    # Constants
    'BUILD_STRATEGY',
    'CREATE_STRATEGY',
    'STUB_STRATEGY',
    'SPLITTER',
    'BuilderPhase',
    # Errors
    'FactoryError',
    'AssociatedClassError',
    'UnknownStrategy',
    'UnsupportedStrategy',
    'CyclicDefinitionError',
    'InvalidDeclarationError',
    # Utilities
    'OrderedBase',
    'ResetableIterator',
    # Random
    'get_random_state',
    'set_random_state',
    'reseed_random',
    # Strategy decorator
    'use_strategy',
]
