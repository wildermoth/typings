"""
Test file to verify LSP comprehension of Pydantic type stubs.

This file tests that type checkers and LSP servers correctly understand:
- Computed fields as properties (not methods)
- Field access returning actual types (not FieldInfo)
- Nested models with proper type inference
- Generic models
- Validators and serializers preserving signatures
- Inheritance chains
"""

from typing import Generic, TypeVar
from pydantic import BaseModel, Field, computed_field, field_validator, field_serializer


# Test 1: Basic field access - LSP should show field types, not FieldInfo
class User(BaseModel):
    name: str
    age: int = Field(ge=0, le=150, description="User age")
    email: str | None = None


def test_basic_fields():
    """LSP should infer:
    - user.name -> str
    - user.age -> int
    - user.email -> str | None
    NOT FieldInfo!
    """
    user = User(name="Alice", age=30, email="alice@example.com")

    # These should all type-check correctly
    name: str = user.name  # ✓ LSP should know this is str
    age: int = user.age    # ✓ LSP should know this is int
    email: str | None = user.email  # ✓ LSP should know this is str | None

    # LSP should autocomplete: user.<name|age|email|model_dump|model_validate|...>
    reveal_type(user.name)  # Should be str
    reveal_type(user.age)   # Should be int


# Test 2: Computed fields - LSP should show these as properties, not methods
class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field  # type: ignore[misc]
    @property
    def area(self) -> float:
        """Computed field - LSP should see this as a property returning float."""
        return self.width * self.height

    @computed_field  # type: ignore[misc]
    @property
    def perimeter(self) -> float:
        """Another computed field."""
        return 2 * (self.width + self.height)


def test_computed_fields():
    """LSP should infer:
    - rect.area -> float (property, not method)
    - rect.perimeter -> float (property, not method)
    """
    rect = Rectangle(width=10.0, height=5.0)

    # These should work WITHOUT calling () - they're properties!
    area: float = rect.area  # ✓ No () needed, LSP should know it's a property
    perimeter: float = rect.perimeter  # ✓ No () needed

    # LSP should NOT suggest rect.area() or rect.perimeter()
    reveal_type(rect.area)  # Should be float, not Callable
    reveal_type(rect.perimeter)  # Should be float, not Callable


# Test 3: Nested models - LSP should drill down through nested structures
class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str | None = None


class Company(BaseModel):
    name: str
    address: Address


class Employee(BaseModel):
    name: str
    employee_id: int
    company: Company
    home_address: Address | None = None


def test_nested_models():
    """LSP should infer through nested models:
    - employee.company.address.city -> str
    - employee.home_address.street -> str | None (because home_address is optional)
    """
    employee = Employee(
        name="Bob",
        employee_id=12345,
        company=Company(
            name="Acme Corp",
            address=Address(street="123 Main St", city="Springfield", country="USA")
        ),
        home_address=Address(street="456 Oak Ave", city="Shelbyville", country="USA")
    )

    # LSP should autocomplete through the chain
    city: str = employee.company.address.city  # ✓ Should work
    street: str = employee.company.address.street  # ✓ Should work

    # Optional nested access
    if employee.home_address:
        home_city: str = employee.home_address.city  # ✓ After narrowing

    reveal_type(employee.company)  # Should be Company
    reveal_type(employee.company.address)  # Should be Address
    reveal_type(employee.company.address.city)  # Should be str


# Test 4: Generic models - LSP should properly substitute type parameters
T = TypeVar('T')


class Container(BaseModel, Generic[T]):
    value: T
    count: int = 1


class GenericPair(BaseModel, Generic[T]):
    first: T
    second: T

    @computed_field  # type: ignore[misc]
    @property
    def both(self) -> tuple[T, T]:
        """Returns both values as a tuple."""
        return (self.first, self.second)


def test_generic_models():
    """LSP should infer:
    - Container[int].value -> int
    - Container[str].value -> str
    - GenericPair[float].both -> tuple[float, float]
    """
    int_container = Container[int](value=42, count=1)
    str_container = Container[str](value="hello")

    # LSP should know the generic type
    int_val: int = int_container.value  # ✓ Should be int
    str_val: str = str_container.value  # ✓ Should be str

    pair = GenericPair[float](first=1.5, second=2.5)
    both: tuple[float, float] = pair.both  # ✓ Should be tuple[float, float]

    reveal_type(int_container.value)  # Should be int
    reveal_type(str_container.value)  # Should be str
    reveal_type(pair.both)  # Should be tuple[float, float]


# Test 5: Inheritance - LSP should understand inherited fields and computed fields
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int

    @computed_field  # type: ignore[misc]
    @property
    def full_name(self) -> str:
        """Full name computed from first and last."""
        return f"{self.first_name} {self.last_name}"


class Student(Person):
    student_id: str
    gpa: float

    @computed_field  # type: ignore[misc]
    @property
    def is_honor_student(self) -> bool:
        """Whether student has honors GPA."""
        return self.gpa >= 3.5


def test_inheritance():
    """LSP should infer:
    - student.first_name -> str (inherited)
    - student.full_name -> str (inherited computed field)
    - student.gpa -> float (own field)
    - student.is_honor_student -> bool (own computed field)
    """
    student = Student(
        first_name="Jane",
        last_name="Doe",
        age=20,
        student_id="S12345",
        gpa=3.8
    )

    # Inherited fields
    name: str = student.first_name  # ✓ Inherited from Person
    full: str = student.full_name   # ✓ Inherited computed field

    # Own fields
    gpa: float = student.gpa  # ✓ Own field
    honors: bool = student.is_honor_student  # ✓ Own computed field

    reveal_type(student.full_name)  # Should be str
    reveal_type(student.is_honor_student)  # Should be bool


# Test 6: Validators - LSP should preserve method signatures
class Product(BaseModel):
    name: str
    price: float
    quantity: int

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        """Validator should preserve signature."""
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_non_negative(cls, v: int) -> int:
        """Another validator."""
        if v < 0:
            raise ValueError('Quantity cannot be negative')
        return v


def test_validators():
    """LSP should understand validator signatures and not confuse them with fields."""
    product = Product(name="Widget", price=9.99, quantity=10)

    # Regular field access
    price: float = product.price  # ✓ Should be float
    qty: int = product.quantity   # ✓ Should be int

    # LSP should NOT suggest calling validators directly on instances
    reveal_type(product.price)  # Should be float, not a validator


# Test 7: Serializers - LSP should preserve method signatures
class Timestamp(BaseModel):
    year: int
    month: int
    day: int

    @field_serializer('year')
    def serialize_year(self, value: int) -> str:
        """Serializer should preserve signature."""
        return str(value)


def test_serializers():
    """LSP should understand serializer signatures."""
    ts = Timestamp(year=2024, month=11, day=20)

    # Regular field access still returns the field type
    year: int = ts.year  # ✓ Should be int (not serialized yet)

    reveal_type(ts.year)  # Should be int on the instance


# Test 8: Complex nested example with computed fields
class Stats(BaseModel):
    wins: int
    losses: int

    @computed_field  # type: ignore[misc]
    @property
    def total_games(self) -> int:
        return self.wins + self.losses

    @computed_field  # type: ignore[misc]
    @property
    def win_rate(self) -> float:
        if self.total_games == 0:
            return 0.0
        return self.wins / self.total_games


class Team(BaseModel):
    name: str
    stats: Stats

    @computed_field  # type: ignore[misc]
    @property
    def is_winning_team(self) -> bool:
        """Team is winning if win rate > 50%."""
        return self.stats.win_rate > 0.5


def test_complex_nested():
    """LSP should handle:
    - team.stats.total_games -> int (nested computed field)
    - team.stats.win_rate -> float (nested computed field)
    - team.is_winning_team -> bool (computed field using nested computed field)
    """
    team = Team(
        name="Champions",
        stats=Stats(wins=15, losses=5)
    )

    # Nested computed field access
    total: int = team.stats.total_games  # ✓ Should be int
    rate: float = team.stats.win_rate    # ✓ Should be float
    winning: bool = team.is_winning_team  # ✓ Should be bool

    reveal_type(team.stats.total_games)  # Should be int
    reveal_type(team.stats.win_rate)     # Should be float
    reveal_type(team.is_winning_team)    # Should be bool


# Test 9: Ensure model_dump and other methods are properly typed
def test_model_methods():
    """LSP should understand all BaseModel methods."""
    user = User(name="Test", age=25)

    # model_dump should return dict[str, Any]
    data: dict[str, Any] = user.model_dump()

    # model_dump_json should return str
    json_str: str = user.model_dump_json()

    # model_validate should return the same type
    validated: User = User.model_validate({"name": "Test2", "age": 30})

    reveal_type(user.model_dump())  # Should be dict[str, Any]
    reveal_type(user.model_dump_json())  # Should be str
    reveal_type(User.model_validate({}))  # Should be User


if __name__ == "__main__":
    print("Running LSP comprehension tests...")
    print("\n✓ All type hints should be correctly understood by LSP!")
    print("✓ Run with: mypy --strict test_lsp_comprehension.py")
    print("✓ Or use your IDE's type checker to verify autocomplete works correctly")
