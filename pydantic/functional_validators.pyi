"""Type stubs for pydantic.functional_validators module.

This module contains decorators and classes for field and model validation.
"""

from __future__ import annotations

import dataclasses
import sys
from functools import partialmethod
from typing import TYPE_CHECKING, Annotated, Any, Callable, Literal, Protocol, TypeVar, Union, overload

from pydantic_core import PydanticUndefined, core_schema
from typing_extensions import Self, TypeAlias

from .annotated_handlers import GetCoreSchemaHandler

if sys.version_info < (3, 11):
    from typing_extensions import Protocol
else:
    from typing import Protocol

__all__ = (
    'AfterValidator',
    'BeforeValidator',
    'PlainValidator',
    'WrapValidator',
    'field_validator',
    'model_validator',
    'SkipValidation',
    'InstanceOf',
    'ValidateAs',
    'ModelWrapValidatorHandler',
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ VALIDATOR CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dataclasses.dataclass(frozen=True)
class AfterValidator:
    """A metadata class that indicates that a validation should be applied after the inner validation logic.

    Attributes:
        func: The validator function.

    Example:
        ```python
        from typing import Annotated
        from pydantic import AfterValidator, BaseModel, ValidationError

        MyInt = Annotated[int, AfterValidator(lambda v: v + 1)]

        class Model(BaseModel):
            a: MyInt

        print(Model(a=1).a)
        #> 2
        ```
    """

    func: core_schema.NoInfoValidatorFunction | core_schema.WithInfoValidatorFunction

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Get the pydantic core schema.

        Args:
            source_type: The source type.
            handler: The core schema handler.

        Returns:
            The core schema.
        """
        ...

    @classmethod
    def _from_decorator(cls, decorator: Any) -> Self:
        """Create an AfterValidator from a decorator.

        Args:
            decorator: A decorator instance.

        Returns:
            A new AfterValidator instance.
        """
        ...

@dataclasses.dataclass(frozen=True)
class BeforeValidator:
    """A metadata class that indicates that a validation should be applied before the inner validation logic.

    Attributes:
        func: The validator function.
        json_schema_input_type: The input type used to generate the appropriate JSON Schema (in validation mode).
            The actual input type is `Any`.

    Example:
        ```python
        from typing import Annotated
        from pydantic import BaseModel, BeforeValidator

        MyInt = Annotated[int, BeforeValidator(lambda v: v + 1)]

        class Model(BaseModel):
            a: MyInt

        print(Model(a=1).a)
        #> 2
        ```
    """

    func: core_schema.NoInfoValidatorFunction | core_schema.WithInfoValidatorFunction
    json_schema_input_type: Any = PydanticUndefined

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Get the pydantic core schema.

        Args:
            source_type: The source type.
            handler: The core schema handler.

        Returns:
            The core schema.
        """
        ...

    @classmethod
    def _from_decorator(cls, decorator: Any) -> Self:
        """Create a BeforeValidator from a decorator.

        Args:
            decorator: A decorator instance.

        Returns:
            A new BeforeValidator instance.
        """
        ...

@dataclasses.dataclass(frozen=True)
class PlainValidator:
    """A metadata class that indicates that a validation should be applied instead of the inner validation logic.

    Attributes:
        func: The validator function.
        json_schema_input_type: The input type used to generate the appropriate JSON Schema (in validation mode).
            The actual input type is `Any`.
    """

    func: core_schema.NoInfoValidatorFunction | core_schema.WithInfoValidatorFunction
    json_schema_input_type: Any = Any

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Get the pydantic core schema.

        Args:
            source_type: The source type.
            handler: The core schema handler.

        Returns:
            The core schema.
        """
        ...

    @classmethod
    def _from_decorator(cls, decorator: Any) -> Self:
        """Create a PlainValidator from a decorator.

        Args:
            decorator: A decorator instance.

        Returns:
            A new PlainValidator instance.
        """
        ...

@dataclasses.dataclass(frozen=True)
class WrapValidator:
    """A metadata class that indicates that a validation should be applied around the inner validation logic.

    Attributes:
        func: The validator function.
        json_schema_input_type: The input type used to generate the appropriate JSON Schema (in validation mode).
            The actual input type is `Any`.
    """

    func: core_schema.NoInfoWrapValidatorFunction | core_schema.WithInfoWrapValidatorFunction
    json_schema_input_type: Any = PydanticUndefined

    def __get_pydantic_core_schema__(self, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Get the pydantic core schema.

        Args:
            source_type: The source type.
            handler: The core schema handler.

        Returns:
            The core schema.
        """
        ...

    @classmethod
    def _from_decorator(cls, decorator: Any) -> Self:
        """Create a WrapValidator from a decorator.

        Args:
            decorator: A decorator instance.

        Returns:
            A new WrapValidator instance.
        """
        ...

# ~~~~~~~~~~~~~~~~~~~~~~~~~ VALIDATOR PROTOCOLS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if TYPE_CHECKING:

    class _OnlyValueValidatorClsMethod(Protocol):
        def __call__(self, cls: Any, value: Any, /) -> Any: ...

    class _V2ValidatorClsMethod(Protocol):
        def __call__(self, cls: Any, value: Any, info: core_schema.ValidationInfo[Any], /) -> Any: ...

    class _OnlyValueWrapValidatorClsMethod(Protocol):
        def __call__(self, cls: Any, value: Any, handler: core_schema.ValidatorFunctionWrapHandler, /) -> Any: ...

    class _V2WrapValidatorClsMethod(Protocol):
        def __call__(
            self,
            cls: Any,
            value: Any,
            handler: core_schema.ValidatorFunctionWrapHandler,
            info: core_schema.ValidationInfo[Any],
            /,
        ) -> Any: ...

    _V2Validator = Union[
        _V2ValidatorClsMethod,
        core_schema.WithInfoValidatorFunction,
        _OnlyValueValidatorClsMethod,
        core_schema.NoInfoValidatorFunction,
    ]

    _V2WrapValidator = Union[
        _V2WrapValidatorClsMethod,
        core_schema.WithInfoWrapValidatorFunction,
        _OnlyValueWrapValidatorClsMethod,
        core_schema.NoInfoWrapValidatorFunction,
    ]

    _PartialClsOrStaticMethod: TypeAlias = Union[classmethod[Any, Any, Any], staticmethod[Any, Any], partialmethod[Any]]

    _V2BeforeAfterOrPlainValidatorType = TypeVar(
        '_V2BeforeAfterOrPlainValidatorType',
        bound=Union[_V2Validator, _PartialClsOrStaticMethod],
    )
    _V2WrapValidatorType = TypeVar('_V2WrapValidatorType', bound=Union[_V2WrapValidator, _PartialClsOrStaticMethod])

FieldValidatorModes: TypeAlias = Literal['before', 'after', 'wrap', 'plain']
"""Type alias for field validator modes."""

# ~~~~~~~~~~~~~~~~~~~~~~~~~ FIELD VALIDATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@overload
def field_validator(
    field: str,
    /,
    *fields: str,
    mode: Literal['wrap'],
    check_fields: bool | None = ...,
    json_schema_input_type: Any = ...,
) -> Callable[[_V2WrapValidatorType], _V2WrapValidatorType]: ...

@overload
def field_validator(
    field: str,
    /,
    *fields: str,
    mode: Literal['before', 'plain'],
    check_fields: bool | None = ...,
    json_schema_input_type: Any = ...,
) -> Callable[[_V2BeforeAfterOrPlainValidatorType], _V2BeforeAfterOrPlainValidatorType]: ...

@overload
def field_validator(
    field: str,
    /,
    *fields: str,
    mode: Literal['after'] = ...,
    check_fields: bool | None = ...,
) -> Callable[[_V2BeforeAfterOrPlainValidatorType], _V2BeforeAfterOrPlainValidatorType]: ...

def field_validator(
    field: str,
    /,
    *fields: str,
    mode: FieldValidatorModes = 'after',
    check_fields: bool | None = None,
    json_schema_input_type: Any = PydanticUndefined,
) -> Callable[[Any], Any]:
    """
    Decorate methods on the class indicating that they should be used to validate fields.

    **Important for LSP/Type Checkers:**
    - The decorator preserves the method signature for inspection
    - Validators are typically classmethods and receive (cls, value) or (cls, value, info)
    - The decorated method can be called directly for testing
    - Return type should match or be compatible with the field type

    Common signatures:
    - mode='after': `def validate(cls, value: T) -> T` or `def validate(cls, value: T, info: ValidationInfo) -> T`
    - mode='before': `def validate(cls, value: Any) -> Any` or `def validate(cls, value: Any, info: ValidationInfo) -> Any`
    - mode='wrap': `def validate(cls, value: Any, handler: ValidatorFunctionWrapHandler) -> T`
    - mode='plain': `def validate(cls, value: Any) -> T`

    Args:
        field: The first field the field_validator should be called on.
        *fields: Additional field(s) the field_validator should be called on.
        mode: Specifies whether to validate the fields before or after validation.
            - 'before': Run before Pydantic's internal validation
            - 'after': Run after Pydantic's internal validation (default)
            - 'wrap': Wrap Pydantic's validation, allowing you to call it conditionally
            - 'plain': Replace Pydantic's validation entirely
        check_fields: Whether to check that the fields actually exist on the model.
        json_schema_input_type: The input type of the function for JSON Schema generation.

    Returns:
        A decorator that preserves the method signature while marking it as a validator.

    Example:
        ```python
        from pydantic import BaseModel, field_validator, ValidationInfo

        class Model(BaseModel):
            name: str
            age: int

            @field_validator('name')
            @classmethod
            def validate_name(cls, v: str) -> str:
                '''LSP should show this takes str and returns str'''
                if not v.strip():
                    raise ValueError('name cannot be empty')
                return v.strip()

            @field_validator('age', mode='before')
            @classmethod
            def parse_age(cls, v: Any) -> int:
                '''Before validators can receive Any and must return compatible type'''
                if isinstance(v, str):
                    return int(v)
                return v
        ```

    Note:
        The decorator returns the same function, so LSP can inspect the signature.
        Use @classmethod before @field_validator for proper cls access.
    """
    ...

# ~~~~~~~~~~~~~~~~~~~~~~~~~ MODEL VALIDATOR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_ModelType = TypeVar('_ModelType')
_ModelTypeCo = TypeVar('_ModelTypeCo', covariant=True)

class ModelWrapValidatorHandler(core_schema.ValidatorFunctionWrapHandler, Protocol[_ModelTypeCo]):
    """@model_validator decorated function handler argument type. This is used when mode='wrap'."""

    def __call__(
        self,
        value: Any,
        outer_location: str | int | None = None,
        /,
    ) -> _ModelTypeCo: ...

class ModelWrapValidatorWithoutInfo(Protocol[_ModelType]):
    """A @model_validator decorated function signature.
    This is used when mode='wrap' and the function does not have info argument.
    """

    def __call__(
        self,
        cls: type[_ModelType],
        value: Any,
        handler: ModelWrapValidatorHandler[_ModelType],
        /,
    ) -> _ModelType: ...

class ModelWrapValidator(Protocol[_ModelType]):
    """A @model_validator decorated function signature. This is used when mode='wrap'."""

    def __call__(
        self,
        cls: type[_ModelType],
        value: Any,
        handler: ModelWrapValidatorHandler[_ModelType],
        info: core_schema.ValidationInfo,
        /,
    ) -> _ModelType: ...

class FreeModelBeforeValidatorWithoutInfo(Protocol):
    """A @model_validator decorated function signature.
    This is used when mode='before' and the function does not have info argument.
    """

    def __call__(
        self,
        value: Any,
        /,
    ) -> Any: ...

class ModelBeforeValidatorWithoutInfo(Protocol):
    """A @model_validator decorated function signature.
    This is used when mode='before' and the function does not have info argument.
    """

    def __call__(
        self,
        cls: Any,
        value: Any,
        /,
    ) -> Any: ...

class FreeModelBeforeValidator(Protocol):
    """A @model_validator decorated function signature. This is used when mode='before'."""

    def __call__(
        self,
        value: Any,
        info: core_schema.ValidationInfo[Any],
        /,
    ) -> Any: ...

class ModelBeforeValidator(Protocol):
    """A @model_validator decorated function signature. This is used when mode='before'."""

    def __call__(
        self,
        cls: Any,
        value: Any,
        info: core_schema.ValidationInfo[Any],
        /,
    ) -> Any: ...

ModelAfterValidatorWithoutInfo = Callable[[_ModelType], _ModelType]
"""A @model_validator decorated function signature. This is used when mode='after'."""

ModelAfterValidator = Callable[[_ModelType, core_schema.ValidationInfo[Any]], _ModelType]
"""A @model_validator decorated function signature. This is used when mode='after'."""

_AnyModelWrapValidator = Union[ModelWrapValidator[_ModelType], ModelWrapValidatorWithoutInfo[_ModelType]]
_AnyModelBeforeValidator = Union[
    FreeModelBeforeValidator, ModelBeforeValidator, FreeModelBeforeValidatorWithoutInfo, ModelBeforeValidatorWithoutInfo
]
_AnyModelAfterValidator = Union[ModelAfterValidator[_ModelType], ModelAfterValidatorWithoutInfo[_ModelType]]

@overload
def model_validator(
    *,
    mode: Literal['wrap'],
) -> Callable[[_AnyModelWrapValidator[_ModelType]], Any]: ...

@overload
def model_validator(
    *,
    mode: Literal['before'],
) -> Callable[[_AnyModelBeforeValidator], Any]: ...

@overload
def model_validator(
    *,
    mode: Literal['after'],
) -> Callable[[_AnyModelAfterValidator[_ModelType]], Any]: ...

def model_validator(
    *,
    mode: Literal['wrap', 'before', 'after'],
) -> Any:
    """
    Decorate model methods for validation purposes.

    **Important for LSP/Type Checkers:**
    - The decorator preserves the method signature for inspection
    - Model validators run on the entire model (not individual fields)
    - Different modes have different signatures:
        - mode='after': `def validate(self) -> Self` - runs after field validation
        - mode='before': `def validate(cls, data: Any) -> Any` - runs before field validation
        - mode='wrap': `def validate(cls, data: Any, handler: ModelWrapValidatorHandler) -> Self`

    Common signatures:
    - mode='after': Receives the fully validated model instance
        - `def validate(self) -> Self`
        - `def validate(self, info: ValidationInfo) -> Self`
    - mode='before': Receives raw input data (dict, object, etc.)
        - `def validate(cls, data: Any) -> Any`
        - `def validate(cls, data: Any, info: ValidationInfo) -> Any`
        - `def validate(data: Any) -> Any` (without cls for free functions)
    - mode='wrap': Can call the default validation or skip it
        - `def validate(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self`
        - `def validate(cls, data: Any, handler: ModelWrapValidatorHandler[Self], info: ValidationInfo) -> Self`

    Args:
        mode: A required string literal that specifies the validation mode.
            - 'after': Run after all field validations (receives validated model instance)
            - 'before': Run before field validations (receives raw input data)
            - 'wrap': Wrap the validation process (can call or skip default validation)

    Returns:
        A decorator that preserves the method signature while marking it as a model validator.

    Examples:
        ```python
        from pydantic import BaseModel, model_validator
        from typing_extensions import Self

        class Square(BaseModel):
            width: float
            height: float

            @model_validator(mode='after')
            def verify_square(self) -> Self:
                '''After validators receive the validated instance and can perform
                cross-field validation. LSP should show this returns Self.'''
                if self.width != self.height:
                    raise ValueError('width and height do not match')
                return self

        class FlexibleModel(BaseModel):
            data: dict[str, Any]

            @model_validator(mode='before')
            @classmethod
            def normalize_data(cls, values: Any) -> dict[str, Any]:
                '''Before validators can transform input data before validation.
                They receive raw input (Any) and return dict for field validation.'''
                if isinstance(values, str):
                    import json
                    return {'data': json.loads(values)}
                return values

        class ConditionalModel(BaseModel):
            value: int

            @model_validator(mode='wrap')
            @classmethod
            def conditional_validation(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
                '''Wrap validators can conditionally call default validation.
                LSP should show handler returns Self.'''
                if isinstance(data, dict) and data.get('skip_validation'):
                    # Skip validation for certain inputs
                    return cls.model_construct(**data)
                # Call default validation
                return handler(data)
        ```

    Note:
        - Use @classmethod for 'before' and 'wrap' modes
        - Use instance method (self) for 'after' mode
        - The decorator preserves signatures, so LSP can show proper types
    """
    ...

# ~~~~~~~~~~~~~~~~~~~~~~~~~ UTILITY CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AnyType = TypeVar('AnyType')

if TYPE_CHECKING:
    InstanceOf = Annotated[AnyType, ...]
    """Generic type for annotating a type that is an instance of a given class."""
else:

    @dataclasses.dataclass
    class InstanceOf:
        """Generic type for annotating a type that is an instance of a given class.

        Example:
            ```python
            from pydantic import BaseModel, InstanceOf

            class Foo:
                ...

            class Bar(BaseModel):
                foo: InstanceOf[Foo]

            Bar(foo=Foo())
            ```
        """

        @classmethod
        def __class_getitem__(cls, item: AnyType) -> AnyType: ...

        @classmethod
        def __get_pydantic_core_schema__(cls, source: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema: ...

if TYPE_CHECKING:
    SkipValidation = Annotated[AnyType, ...]
    """If this is applied as an annotation, validation will be skipped."""
else:

    @dataclasses.dataclass
    class SkipValidation:
        """If this is applied as an annotation, validation will be skipped.

        This can be useful if you want to use a type annotation for documentation/IDE purposes,
        and know that it is safe to skip validation for one or more of the fields.

        Example:
            ```python
            from typing import Annotated
            from pydantic import BaseModel, SkipValidation

            class Model(BaseModel):
                a: Annotated[int, SkipValidation]

            m = Model(a='not an int')  # No validation error
            ```
        """

        def __class_getitem__(cls, item: Any) -> Any: ...

        @classmethod
        def __get_pydantic_core_schema__(cls, source: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema: ...

_FromTypeT = TypeVar('_FromTypeT')

class ValidateAs:
    """A helper class to validate a custom type from a type that is natively supported by Pydantic.

    This class allows you to validate using one type (like a Pydantic model) and then convert
    the validated result into another type using an instantiation hook.

    Attributes:
        from_type: The type natively supported by Pydantic to use to perform validation.
        instantiation_hook: A callable taking the validated type as an argument, and returning
            the populated custom type.

    Example:
        ```python
        from typing import Annotated
        from pydantic import BaseModel, TypeAdapter, ValidateAs

        class MyCls:
            def __init__(self, a: int) -> None:
                self.a = a

            def __repr__(self) -> str:
                return f"MyCls(a={self.a})"

        class Model(BaseModel):
            a: int

        ta = TypeAdapter(
            Annotated[MyCls, ValidateAs(Model, lambda v: MyCls(a=v.a))]
        )

        print(ta.validate_python({'a': 1}))
        #> MyCls(a=1)
        ```
    """

    from_type: type[_FromTypeT]
    instantiation_hook: Callable[[_FromTypeT], Any]

    def __init__(self, from_type: type[_FromTypeT], /, instantiation_hook: Callable[[_FromTypeT], Any]) -> None:
        """Initialize ValidateAs.

        Args:
            from_type: The type natively supported by Pydantic to use to perform validation.
            instantiation_hook: A callable taking the validated type as an argument, and returning
                the populated custom type.
        """
        ...

    def __get_pydantic_core_schema__(self, source: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """Get the pydantic core schema for this ValidateAs instance.

        Args:
            source: The source type.
            handler: The GetCoreSchemaHandler instance.

        Returns:
            The pydantic core schema.
        """
        ...
