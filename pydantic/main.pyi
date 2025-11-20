"""Type stubs for pydantic.main module containing BaseModel and related functions."""

from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generator,
    Generic,
    Literal,
    Mapping,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)
from typing_extensions import Self, TypeAlias, Unpack, dataclass_transform

from pydantic_core import CoreSchema, SchemaSerializer, SchemaValidator
from pydantic_core.core_schema import ValidationError

from .config import ConfigDict, ExtraValues
from .fields import ComputedFieldInfo, Field, FieldInfo, ModelPrivateAttr
from .json_schema import (
    DEFAULT_REF_TEMPLATE,
    GenerateJsonSchema,
    JsonSchemaMode,
    JsonSchemaValue,
)

_T = TypeVar("_T")
_Model = TypeVar("_Model", bound="BaseModel")

# Type aliases
TupleGenerator: TypeAlias = Generator[tuple[str, Any], None, None]
IncEx: TypeAlias = Union[
    set[int],
    set[str],
    Mapping[int, Union[IncEx, bool]],
    Mapping[str, Union[IncEx, bool]]
]

__all__ = ("BaseModel", "create_model")

@dataclass_transform(kw_only_default=True, field_specifiers=(Field,))
class BaseModel:
    """
    Base class for all Pydantic models.

    Usage Documentation: https://docs.pydantic.dev/latest/concepts/models/

    A base class for creating Pydantic models with automatic validation.

    BaseModel uses a metaclass (ModelMetaclass) to enable:
    - Automatic validation of data against type hints
    - Descriptor protocol for fields (FieldInfo on class, actual values on instances)
    - Generic model support via __class_getitem__
    - Computed fields via @computed_field decorator

    When you define a field on a BaseModel:
    - On the class: accessing the field returns FieldInfo metadata
    - On an instance: accessing the field returns the validated value

    Example:
        ```python
        from pydantic import BaseModel, Field

        class User(BaseModel):
            name: str
            age: int = Field(ge=0, description="User's age")

        # On class: User.age returns FieldInfo
        # On instance: user.age returns the int value
        user = User(name="Alice", age=30)
        assert user.age == 30  # Returns int, not FieldInfo
        ```

    Attributes:
        model_config: Configuration dictionary for the model.
        model_fields: Dictionary of field names and their FieldInfo objects.
        model_computed_fields: Dictionary of computed field names and their ComputedFieldInfo objects.
        model_extra: Extra fields set during validation (if config.extra='allow').
        model_fields_set: Names of fields explicitly set during instantiation.
    """

    # Class variables set by metaclass (ModelMetaclass)
    model_config: ClassVar[ConfigDict]
    __class_vars__: ClassVar[set[str]]
    __private_attributes__: ClassVar[Dict[str, ModelPrivateAttr]]
    __pydantic_complete__: ClassVar[bool]
    __pydantic_core_schema__: ClassVar[CoreSchema]
    __pydantic_custom_init__: ClassVar[bool]
    __pydantic_decorators__: ClassVar[Any]
    __pydantic_generic_metadata__: ClassVar[Any]
    __pydantic_parent_namespace__: ClassVar[Dict[str, Any] | None]
    __pydantic_post_init__: ClassVar[None | Literal["model_post_init"]]
    __pydantic_root_model__: ClassVar[bool]
    __pydantic_serializer__: ClassVar[SchemaSerializer]
    __pydantic_validator__: ClassVar[SchemaValidator]
    __pydantic_fields__: ClassVar[Dict[str, FieldInfo]]
    __pydantic_computed_fields__: ClassVar[Dict[str, ComputedFieldInfo]]

    # Instance variables
    __pydantic_extra__: Dict[str, Any] | None
    __pydantic_fields_set__: set[str]
    __pydantic_private__: Dict[str, Any] | None

    def __init__(self, /, **data: Any) -> None:
        """
        Create a new model by parsing and validating input data from keyword arguments.

        Raises:
            ValidationError: If the input data cannot be validated.
        """
        ...

    @classmethod
    @property
    def model_fields(cls) -> dict[str, FieldInfo]:
        """
        A mapping of field names to their respective FieldInfo instances.

        Warning:
            Accessing this attribute from a model instance is deprecated.
            Access from the model class instead.
        """
        ...

    @classmethod
    @property
    def model_computed_fields(cls) -> dict[str, ComputedFieldInfo]:
        """
        A mapping of computed field names to their respective ComputedFieldInfo instances.

        Warning:
            Accessing this attribute from a model instance is deprecated.
            Access from the model class instead.
        """
        ...

    @property
    def model_extra(self) -> dict[str, Any] | None:
        """
        Get extra fields set during validation.

        Returns:
            A dictionary of extra fields, or None if config.extra is not set to 'allow'.
        """
        ...

    @property
    def model_fields_set(self) -> set[str]:
        """
        Returns the set of fields that have been explicitly set on this model instance.

        Returns:
            A set of strings representing the fields that were set.
        """
        ...

    @classmethod
    def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:
        """
        Creates a new instance of the Model class with validated data.

        Creates a new model setting __dict__ and __pydantic_fields_set__ from trusted
        or pre-validated data. Default values are respected, but no other validation
        is performed.

        Args:
            _fields_set: A set of field names that were originally explicitly set.
                If provided, this is directly used for the model_fields_set attribute.
            values: Trusted or pre-validated data dictionary.

        Returns:
            A new instance of the Model class with validated data.
        """
        ...

    def model_copy(
        self,
        *,
        update: Mapping[str, Any] | None = None,
        deep: bool = False
    ) -> Self:
        """
        Returns a copy of the model.

        Args:
            update: Values to change/add in the new model.
            deep: Set to True to make a deep copy of the model.

        Returns:
            New model instance.
        """
        ...

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        """
        Generate a dictionary representation of the model.

        Args:
            mode: The mode in which to_python should run ('json' or 'python').
            include: A set of fields to include in the output.
            exclude: A set of fields to exclude from the output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to use the field's alias in the dictionary key.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of None.
            exclude_computed_fields: Whether to exclude computed fields.
            round_trip: If True, dumped values should be valid as input for non-idempotent types.
            warnings: How to handle serialization errors.
            fallback: A function to call when an unknown value is encountered.
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A dictionary representation of the model.
        """
        ...

    def model_dump_json(
        self,
        *,
        indent: int | None = None,
        ensure_ascii: bool = False,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
    ) -> str:
        """
        Generates a JSON representation of the model using Pydantic's to_json method.

        Args:
            indent: Indentation to use in the JSON output.
            ensure_ascii: If True, all incoming non-ASCII characters are escaped.
            include: Field(s) to include in the JSON output.
            exclude: Field(s) to exclude from the JSON output.
            context: Additional context to pass to the serializer.
            by_alias: Whether to serialize using field aliases.
            exclude_unset: Whether to exclude fields that have not been explicitly set.
            exclude_defaults: Whether to exclude fields that are set to their default value.
            exclude_none: Whether to exclude fields that have a value of None.
            exclude_computed_fields: Whether to exclude computed fields.
            round_trip: If True, dumped values should be valid as input for non-idempotent types.
            warnings: How to handle serialization errors.
            fallback: A function to call when an unknown value is encountered.
            serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

        Returns:
            A JSON string representation of the model.
        """
        ...

    @classmethod
    def model_json_schema(
        cls,
        by_alias: bool = True,
        ref_template: str = DEFAULT_REF_TEMPLATE,
        schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
        mode: JsonSchemaMode = "validation",
        *,
        union_format: Literal["any_of", "primitive_type_array"] = "any_of",
    ) -> dict[str, Any]:
        """
        Generates a JSON schema for a model class.

        Args:
            by_alias: Whether to use attribute aliases or not.
            ref_template: The reference template.
            schema_generator: To override the logic used to generate the JSON schema.
            mode: The mode in which to generate the schema.
            union_format: The format to use when combining schemas from unions together.

        Returns:
            The JSON schema for the given model class.
        """
        ...

    @classmethod
    def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:
        """
        Compute the class name for parametrizations of generic classes.

        Args:
            params: Tuple of types of the class.

        Returns:
            String representing the new class where params are passed to cls as type variables.

        Raises:
            TypeError: Raised when trying to generate concrete names for non-generic models.
        """
        ...

    def model_post_init(self, context: Any, /) -> None:
        """
        Override this method to perform additional initialization after __init__ and model_construct.

        This is useful if you want to do some validation that requires the entire model
        to be initialized.
        """
        ...

    @classmethod
    def model_rebuild(
        cls,
        *,
        force: bool = False,
        raise_errors: bool = True,
        _parent_namespace_depth: int = 2,
        _types_namespace: Any | None = None,
    ) -> bool | None:
        """
        Try to rebuild the pydantic-core schema for the model.

        This may be necessary when one of the annotations is a ForwardRef which could not
        be resolved during the initial attempt to build the schema.

        Args:
            force: Whether to force the rebuilding of the model schema.
            raise_errors: Whether to raise errors.
            _parent_namespace_depth: The depth level of the parent namespace.
            _types_namespace: The types namespace.

        Returns:
            Returns None if the schema is already complete and rebuilding was not required.
            If rebuilding was required, returns True if rebuilding was successful, otherwise False.
        """
        ...

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        """
        Validate a pydantic model instance.

        Args:
            obj: The object to validate.
            strict: Whether to enforce types strictly.
            extra: Whether to ignore, allow, or forbid extra data during model validation.
            from_attributes: Whether to extract data from object attributes.
            context: Additional context to pass to the validator.
            by_alias: Whether to use the field's alias when validating.
            by_name: Whether to use the field's name when validating.

        Raises:
            ValidationError: If the object could not be validated.

        Returns:
            The validated model instance.
        """
        ...

    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        """
        Validate the given JSON data against the Pydantic model.

        Args:
            json_data: The JSON data to validate.
            strict: Whether to enforce types strictly.
            extra: Whether to ignore, allow, or forbid extra data.
            context: Extra variables to pass to the validator.
            by_alias: Whether to use the field's alias when validating.
            by_name: Whether to use the field's name when validating.

        Returns:
            The validated Pydantic model.

        Raises:
            ValidationError: If json_data is not a JSON string or validation fails.
        """
        ...

    @classmethod
    def model_validate_strings(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self:
        """
        Validate the given object with string data against the Pydantic model.

        Args:
            obj: The object containing string data to validate.
            strict: Whether to enforce types strictly.
            extra: Whether to ignore, allow, or forbid extra data.
            context: Extra variables to pass to the validator.
            by_alias: Whether to use the field's alias when validating.
            by_name: Whether to use the field's name when validating.

        Returns:
            The validated Pydantic model.
        """
        ...

    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    def __delattr__(self, name: str) -> None: ...
    def __copy__(self) -> Self: ...
    def __deepcopy__(self, memo: dict[int, Any] | None = None) -> Self: ...
    def __rich_repr__(self) -> TupleGenerator: ...
    @classmethod
    def __class_getitem__(
        cls, typevar_values: type[Any] | tuple[type[Any], ...]
    ) -> type[Self]:
        """
        Support for generic models via subscript syntax.

        Allows creating parameterized versions of generic models:
            GenericModel[int], GenericModel[str, float], etc.

        Args:
            typevar_values: Type parameter(s) for the generic model.

        Returns:
            A new model class with the specified type parameters.

        Example:
            ```python
            from typing import Generic, TypeVar
            from pydantic import BaseModel

            T = TypeVar('T')

            class GenericModel(BaseModel, Generic[T]):
                value: T

            IntModel = GenericModel[int]
            instance = IntModel(value=42)
            ```
        """
        ...


def create_model(
    __model_name: str,
    *,
    __config__: ConfigDict | None = None,
    __doc__: str | None = None,
    __base__: type[BaseModel] | tuple[type[BaseModel], ...] | None = None,
    __module__: str = __name__,
    __validators__: dict[str, Any] | None = None,
    __cls_kwargs__: dict[str, Any] | None = None,
    **field_definitions: Any,
) -> type[BaseModel]:
    """
    Dynamically create a new Pydantic model.

    Args:
        __model_name: The name of the model to create.
        __config__: The config dict for the new model.
        __doc__: The docstring for the new model.
        __base__: The base class(es) for the new model.
        __module__: The module name for the new model.
        __validators__: A dict of validators for the new model.
        __cls_kwargs__: Additional keyword arguments to pass to the model metaclass.
        **field_definitions: Field definitions for the new model.

    Returns:
        A new Pydantic model class.

    Example:
        ```python
        from pydantic import create_model

        DynamicModel = create_model(
            'DynamicModel',
            name=(str, ...),
            age=(int, 0)
        )

        m = DynamicModel(name='John', age=30)
        ```
    """
    ...
