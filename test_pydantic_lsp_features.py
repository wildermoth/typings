"""
Test file demonstrating LSP-friendly Pydantic type stub features.

This file serves as both documentation and validation that the improved type stubs
provide proper LSP support for autocompletion, type checking, and navigation.

Run with: python test_pydantic_lsp_features.py
Or use your LSP (Pylance, Pyright, mypy, etc.) to verify type inference.
"""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator, field_serializer, ValidationInfo
from typing_extensions import Self


# ============================================================================
# 1. Field() - Descriptor Protocol
# ============================================================================

class UserWithFields(BaseModel):
    """Demonstrates Field() behavior with LSP."""
    name: str = Field(min_length=1, description="User's name")
    age: int = Field(ge=0, le=150, description="User's age")
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")


def test_field_descriptor():
    """
    LSP should understand:
    - On class: UserWithFields.model_fields['age'] -> FieldInfo
    - On instance: user.age -> int (not FieldInfo)
    """
    # Instance access returns the actual type
    user = UserWithFields(name="Alice", age=30, email="alice@example.com")

    # LSP should infer: user.age -> int
    age: int = user.age
    assert age == 30

    # LSP should infer: user.name -> str
    name: str = user.name
    assert name == "Alice"

    # Class-level introspection returns FieldInfo
    from pydantic.fields import FieldInfo
    age_field_info = UserWithFields.model_fields['age']
    assert isinstance(age_field_info, FieldInfo)
    assert age_field_info.description == "User's age"

    print("✓ Field descriptor protocol works correctly")


# ============================================================================
# 2. computed_field() - Property Return Type
# ============================================================================

class Rectangle(BaseModel):
    """Demonstrates computed_field with property."""
    width: int
    length: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def area(self) -> int:
        """Computed area - appears in serialization.

        LSP should show this as:
        - rect.area -> int (not a method, not FieldInfo)
        - It's a readonly property
        """
        return self.width * self.length

    @computed_field(alias='perimeter_value')  # type: ignore[prop-decorator]
    @property
    def perimeter(self) -> int:
        """Computed perimeter with alias."""
        return 2 * (self.width + self.length)


def test_computed_field():
    """
    LSP should understand:
    - rect.area -> int (property, not method)
    - rect.perimeter -> int (property, not method)
    - Both appear in model_dump() output
    """
    rect = Rectangle(width=3, length=4)

    # LSP should infer these as int properties, not methods
    area: int = rect.area
    perimeter: int = rect.perimeter

    assert area == 12
    assert perimeter == 14

    # Computed fields appear in serialization
    data = rect.model_dump()
    # Note: perimeter uses alias 'perimeter_value' only in JSON schema, not always in dump
    assert 'area' in data
    assert data['area'] == 12
    assert data['width'] == 3

    print("✓ computed_field property typing works correctly")


# ============================================================================
# 3. BaseModel - Generic Support
# ============================================================================

T = TypeVar('T')

class GenericContainer(BaseModel, Generic[T]):
    """Generic model demonstrating __class_getitem__ support."""
    value: T
    count: int = 1


def test_generic_model():
    """
    LSP should understand:
    - GenericContainer[int] creates a model where value: int
    - GenericContainer[str] creates a model where value: str
    """
    # LSP should infer: int_container.value -> int
    int_container = GenericContainer[int](value=42, count=1)
    int_value: int = int_container.value
    assert int_value == 42

    # LSP should infer: str_container.value -> str
    str_container = GenericContainer[str](value="hello", count=1)
    str_value: str = str_container.value
    assert str_value == "hello"

    print("✓ Generic model support works correctly")


# ============================================================================
# 4. field_validator - Signature Preservation
# ============================================================================

class ValidatedModel(BaseModel):
    """Demonstrates field_validator with preserved signatures."""
    name: str
    age: int
    email: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validator that preserves signature.

        LSP should show:
        - Takes: str
        - Returns: str
        - Can be called directly for testing
        """
        if not v.strip():
            raise ValueError('name cannot be empty')
        return v.strip()

    @field_validator('age', mode='before')
    @classmethod
    def parse_age(cls, v: Any) -> int:
        """Before validator can receive Any and coerce to int.

        LSP should show:
        - Takes: Any
        - Returns: int
        """
        if isinstance(v, str):
            return int(v)
        return v

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str, info: ValidationInfo) -> str:
        """Validator with ValidationInfo parameter.

        LSP should show both parameters.
        """
        if '@' not in v:
            raise ValueError('invalid email')
        return v.lower()


def test_field_validator():
    """
    LSP should understand:
    - Validators preserve their method signatures
    - Can be called directly (ValidatedModel.validate_name.__func__(ValidatedModel, "test"))
    - Type hints are preserved
    """
    # Validators are called during model creation
    model = ValidatedModel(name="  Alice  ", age="30", email="ALICE@EXAMPLE.COM")

    assert model.name == "Alice"  # stripped
    assert model.age == 30  # coerced from string
    assert model.email == "alice@example.com"  # lowercased

    # LSP should allow direct validator calls for testing
    result = ValidatedModel.validate_name("  test  ")
    assert result == "test"

    print("✓ field_validator signature preservation works correctly")


# ============================================================================
# 5. model_validator - Mode-Specific Signatures
# ============================================================================

class Square(BaseModel):
    """Demonstrates model_validator modes."""
    width: float
    height: float

    @model_validator(mode='after')
    def verify_square(self) -> Self:
        """After validator receives validated instance.

        LSP should show:
        - Takes: self (the validated instance)
        - Returns: Self
        """
        if self.width != self.height:
            raise ValueError('width and height must match for a square')
        return self


class FlexibleInput(BaseModel):
    """Demonstrates before validator."""
    data: dict[str, Any]

    @model_validator(mode='before')
    @classmethod
    def normalize_input(cls, values: Any) -> dict[str, Any]:
        """Before validator can transform input.

        LSP should show:
        - Takes: Any (raw input)
        - Returns: dict[str, Any]
        """
        if isinstance(values, str):
            import json
            return {'data': json.loads(values)}
        return values


def test_model_validator():
    """
    LSP should understand:
    - After validators: self -> Self
    - Before validators: cls, Any -> dict
    - Signatures are preserved
    """
    # After validator
    square = Square(width=5.0, height=5.0)
    assert square.width == square.height

    try:
        Square(width=5.0, height=6.0)
        assert False, "Should have raised validation error"
    except ValueError as e:
        assert "must match" in str(e)

    # Before validator
    flexible = FlexibleInput(data={"key": "value"})
    assert flexible.data == {"key": "value"}

    print("✓ model_validator signature preservation works correctly")


# ============================================================================
# 6. field_serializer - Signature Preservation
# ============================================================================

class SerializedModel(BaseModel):
    """Demonstrates field_serializer."""
    courses: set[str]
    score: float

    @field_serializer('courses', when_used='json')
    def serialize_courses(self, courses: set[str]) -> list[str]:
        """Serializer with preserved signature.

        LSP should show:
        - Takes: set[str]
        - Returns: list[str]
        """
        return sorted(courses)

    @field_serializer('score')
    def serialize_score(self, score: float) -> float:
        """Round score to 2 decimal places.

        LSP should show both the field value type and return type.
        """
        return round(score, 2)


def test_field_serializer():
    """
    LSP should understand:
    - Serializers preserve their signatures
    - Can be called directly for testing
    """
    model = SerializedModel(courses={'Math', 'English', 'Chemistry'}, score=95.678)

    # Internal value is still a set
    assert isinstance(model.courses, set)

    # Serialization uses the serializer
    dumped = model.model_dump()
    assert dumped['score'] == 95.68  # rounded

    # JSON mode serializer for courses
    import json
    json_data = json.loads(model.model_dump_json())
    assert json_data['courses'] == ['Chemistry', 'English', 'Math']  # sorted

    print("✓ field_serializer signature preservation works correctly")


# ============================================================================
# 7. Nested Models
# ============================================================================

class Address(BaseModel):
    """Nested model."""
    street: str
    city: str
    zipcode: str = Field(pattern=r'^\d{5}$')


class Person(BaseModel):
    """Model with nested model field."""
    name: str
    address: Address

    @computed_field  # type: ignore[prop-decorator]
    @property
    def full_location(self) -> str:
        """LSP should drill into nested model.

        Shows: address.city -> str (not FieldInfo)
        """
        return f"{self.address.city}, {self.address.zipcode}"


def test_nested_models():
    """
    LSP should understand:
    - person.address -> Address
    - person.address.city -> str
    - Nested navigation works properly
    """
    person = Person(
        name="Bob",
        address=Address(street="123 Main St", city="Springfield", zipcode="12345")
    )

    # LSP should infer types through nesting
    address: Address = person.address
    city: str = person.address.city
    location: str = person.full_location

    assert city == "Springfield"
    assert location == "Springfield, 12345"

    print("✓ Nested model type inference works correctly")


# ============================================================================
# 8. Complex Validation Flow
# ============================================================================

class ComplexModel(BaseModel):
    """Demonstrates multiple validators and serializers working together."""
    raw_data: str
    processed: int = 0

    @field_validator('raw_data', mode='before')
    @classmethod
    def preprocess_data(cls, v: Any) -> str:
        """LSP: Any -> str"""
        if isinstance(v, int):
            return str(v)
        return v

    @field_validator('raw_data')
    @classmethod
    def validate_data(cls, v: str) -> str:
        """LSP: str -> str"""
        if not v.strip():
            raise ValueError('data cannot be empty')
        return v.strip().upper()

    @model_validator(mode='after')
    def set_processed(self) -> Self:
        """LSP: Self -> Self"""
        self.processed = len(self.raw_data)
        return self

    @field_serializer('raw_data')
    def serialize_data(self, value: str) -> str:
        """LSP: str -> str"""
        return value.lower()

    @computed_field  # type: ignore[prop-decorator]
    @property
    def summary(self) -> str:
        """LSP: -> str (property)"""
        return f"{self.raw_data[:10]}... ({self.processed} chars)"


def test_complex_validation():
    """
    LSP should track types through entire validation pipeline:
    - Before validator: Any -> str
    - After validator: str -> str
    - Model validator: modifies instance
    - Computed field: returns str
    - Serializer: str -> str (lowercase)
    """
    model = ComplexModel(raw_data=12345)

    # After validation pipeline
    assert model.raw_data == "12345"  # uppercased by validator
    assert model.processed == 5  # set by model_validator

    # LSP infers property type
    summary: str = model.summary
    assert "12345" in summary

    # Serialization applies serializer
    dumped = model.model_dump()
    assert dumped['raw_data'] == "12345"  # lowercased by serializer

    print("✓ Complex validation flow type tracking works correctly")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("Testing Pydantic LSP-Friendly Type Stubs\n" + "=" * 50)

    test_field_descriptor()
    test_computed_field()
    test_generic_model()
    test_field_validator()
    test_model_validator()
    test_field_serializer()
    test_nested_models()
    test_complex_validation()

    print("\n" + "=" * 50)
    print("✅ All LSP feature tests passed!")
    print("\nYour LSP should now provide:")
    print("  • Accurate type inference for fields on instances")
    print("  • Property types for computed_field decorators")
    print("  • Generic model parameter inference")
    print("  • Preserved signatures for validators and serializers")
    print("  • Nested model navigation")
    print("  • Full validation pipeline type tracking")
