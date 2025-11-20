# Pydantic Type Stubs - LSP Analysis

This document explains how LSP (Language Server Protocol) servers will interpret the Pydantic type stubs and what works vs. what has inherent limitations.

## ✅ What Works Perfectly

### 1. **Computed Fields as Properties**
```python
class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height
```

**LSP Behavior:**
- ✅ `rect.area` → `float` (not `() -> float`)
- ✅ Autocomplete shows `area` as a property, not a method
- ✅ No `()` required to access the value
- ✅ Type inference works: `area_val: float = rect.area`

**How it works:** `computed_field()` returns `PropertyT` which preserves the `property` type, so LSP sees it as a property descriptor.

### 2. **Nested Model Navigation**
```python
class Address(BaseModel):
    city: str

class Person(BaseModel):
    address: Address

person.address.city  # LSP knows this is `str`
```

**LSP Behavior:**
- ✅ Full autocomplete chain: `person.` → `address` → `.city`
- ✅ Type inference through nesting
: `city: str = person.address.city`
- ✅ Works with optional fields after narrowing

### 3. **Generic Models**
```python
T = TypeVar('T')

class Container(BaseModel, Generic[T]):
    value: T

int_container = Container[int](value=42)
int_container.value  # LSP knows this is `int`
```

**LSP Behavior:**
- ✅ Type parameter substitution works
- ✅ `Container[int].value` → `int`
- ✅ `Container[str].value` → `str`
- ✅ Nested generics work: `Container[List[int]]`

**How it works:** `BaseModel.__class_getitem__` is properly typed to return `type[Self]`.

### 4. **Model Methods**
```python
user = User(name="Alice", age=30)
data = user.model_dump()  # LSP knows this is dict[str, Any]
json_str = user.model_dump_json()  # LSP knows this is str
```

**LSP Behavior:**
- ✅ All `BaseModel` methods have complete signatures
- ✅ Return types are properly typed
- ✅ Parameters have proper types and defaults
- ✅ Docstrings show in hover information

### 5. **Inheritance**
```python
class Person(BaseModel):
    name: str

class Student(Person):
    student_id: str

student.name  # LSP knows this is `str` (inherited)
```

**LSP Behavior:**
- ✅ Inherited fields are recognized
- ✅ Inherited computed fields work
- ✅ Method resolution order is correct
- ✅ Autocomplete shows all fields (own + inherited)

### 6. **Validators Preserve Signatures**
```python
class Product(BaseModel):
    price: float

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        return v
```

**LSP Behavior:**
- ✅ Validator method signature is preserved
- ✅ LSP understands it's a classmethod
- ✅ Parameter and return types are correct
- ✅ Doesn't confuse validator with the field itself

## ⚠️ Inherent Limitations (Python/LSP, not stub issues)

### 1. **Field Access - Class vs Instance**

```python
class User(BaseModel):
    age: int = Field(ge=0)

# On class:
User.age  # Actually FieldInfo, but type checkers may struggle here

# On instance:
user = User(age=30)
user.age  # This is `int` - works correctly!
```

**The Challenge:**
- At runtime, Python uses the descriptor protocol
- `BaseModel.__getattribute__` returns different types for class vs instance access
- Static type checkers can't fully model this without descriptor protocol support

**Current Stub Behavior:**
- ✅ Instance access (`user.age`) works perfectly - LSP sees `int`
- ⚠️ Class access (`User.age`) may show as the field type, not `FieldInfo`
- This is a limitation of PEP 681 `@dataclass_transform` - it tells type checkers to treat fields as their types, not descriptors

**Why this is acceptable:**
- 99% of code accesses fields on instances, not classes
- When you need metadata, you use `User.model_fields['age']` explicitly
- This matches how `@dataclass` works in stdlib

### 2. **Field() Return Type**

```python
class User(BaseModel):
    # Field() returns FieldInfo, but type checkers see it as int
    age: int = Field(default=0)
```

**The Design:**
- `Field()` actually returns `FieldInfo` at runtime
- But `@dataclass_transform` tells LSP to treat it as the annotated type
- This is intentional - it makes type checking work like dataclasses

**Overloads we have:**
```python
@overload
def Field(default: type[...]) -> Any: ...  # For Field(...)

@overload
def Field(default: Any, *, validate_default: Literal[True]) -> Any: ...

@overload
def Field(default: _T) -> _T: ...  # Type inference from default

@overload
def Field(*, default_factory: Callable[[], _T]) -> _T: ...  # From factory
```

**Why this works:**
- LSP uses the annotation (`age: int`) for the field type
- `Field()` is metadata, not the actual value
- Matches standard Python typing philosophy

### 3. **Dynamic Model Creation**

```python
DynamicModel = create_model('DynamicModel', name=(str, ...))
instance = DynamicModel(name="test")
instance.name  # LSP may not know this is `str`
```

**Why it's limited:**
- `create_model()` creates models at runtime
- LSP can't analyze runtime code
- Return type is `type[BaseModel]` - can't be more specific

**Workaround:**
```python
# For LSP, define a proper class
class DynamicModel(BaseModel):
    name: str

# Or use type: ignore for dynamic models
instance = create_model(...)  # type: ignore
```

## 🎯 Best Practices for LSP-Friendly Code

### 1. **Always use type annotations**
```python
# Good - LSP knows everything
class User(BaseModel):
    name: str
    age: int

# Bad - LSP knows nothing
class User(BaseModel):
    name = Field(default="unknown")  # Missing annotation!
```

### 2. **Use computed_field correctly**
```python
# Good - LSP sees as property
class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:  # ← Return type annotation!
        return self.width * self.height

# Bad - missing @property
@computed_field
def area(self) -> float:  # This becomes a method, not a property!
    return self.width * self.height
```

### 3. **Generic models need TypeVar**
```python
from typing import Generic, TypeVar

T = TypeVar('T')

# Good - LSP can track T
class Container(BaseModel, Generic[T]):
    value: T

# Then use it
IntContainer = Container[int]
```

### 4. **Nested models need explicit types**
```python
# Good - LSP can navigate
class Address(BaseModel):
    city: str

class Person(BaseModel):
    address: Address  # Explicit type

# Bad - dynamic/forward ref issues
class Person(BaseModel):
    address: 'Address'  # String annotation may confuse LSP
```

### 5. **Validators should have type annotations**
```python
# Good - LSP understands
@field_validator('price')
@classmethod
def validate_price(cls, v: float) -> float:
    return v

# Acceptable - works but less clear
@field_validator('price')
@classmethod
def validate_price(cls, v):  # LSP infers from field annotation
    return v
```

## 📊 Summary Table

| Feature | LSP Support | Notes |
|---------|-------------|-------|
| Field access on instances | ✅ Perfect | `user.age` → `int` |
| Field access on classes | ⚠️ Limited | `User.age` may not show as `FieldInfo` |
| Computed fields | ✅ Perfect | Shows as properties |
| Nested models | ✅ Perfect | Full autocomplete chain |
| Generic models | ✅ Perfect | Type parameter substitution works |
| Inheritance | ✅ Perfect | All inherited members visible |
| Validators | ✅ Perfect | Signatures preserved |
| Serializers | ✅ Perfect | Signatures preserved |
| Model methods | ✅ Perfect | All typed correctly |
| Dynamic models | ❌ Not possible | Runtime creation can't be analyzed |

## 🔍 How to Verify LSP Behavior

### Using Pyright/Pylance (VS Code)
1. Open the test file in VS Code
2. Hover over variables - should show inferred types
3. Use autocomplete - should show all fields and methods
4. Use "Go to Definition" - should navigate correctly

### Using mypy
```bash
mypy --strict test_lsp_comprehension.py
```

Should type-check successfully with no errors for valid code.

### Using reveal_type
```python
from typing import reveal_type

user = User(name="Alice", age=30)
reveal_type(user.age)  # Should show: int
```

## 🚀 Conclusion

The Pydantic type stubs are **maximally LSP-friendly** within the constraints of Python's static typing system:

- ✅ All common use cases work perfectly
- ✅ Computed fields are properly typed as properties
- ✅ Nested models and generics work correctly
- ✅ Inheritance and method resolution work
- ⚠️ Minor limitations exist for class-level field access (acceptable trade-off)
- ❌ Dynamic model creation can't be statically analyzed (inherent limitation)

For 99% of Pydantic usage, LSP will provide excellent autocomplete, type checking, and navigation!
