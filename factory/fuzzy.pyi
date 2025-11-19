"""
Type stubs for factory.fuzzy module.

Fuzzy attributes for generating random values.
"""

import datetime
import decimal
from typing import Any, Callable, Dict, Iterable, Sequence, TypeVar
from . import builder, declarations

_T = TypeVar('_T')

class BaseFuzzyAttribute(declarations.BaseDeclaration):
    """
    Base class for fuzzy attributes.

    Subclasses should override the fuzz() method to provide random values.
    """
    def fuzz(self) -> Any:
        """Generate a random value."""
        ...

    def evaluate(
        self,
        instance: Any,
        step: builder.BuildStep,
        extra: Dict[str, Any]
    ) -> Any: ...

class FuzzyAttribute(BaseFuzzyAttribute):
    """
    Generate random values using a custom function.

    Example:
        import random
        value = factory.FuzzyAttribute(lambda: random.choice(['a', 'b', 'c']))
    """
    fuzzer: Callable[[], _T]

    def __init__(self, fuzzer: Callable[[], _T]) -> None:
        """
        Initialize with a fuzzer function.

        Args:
            fuzzer: A callable that takes no arguments and returns a random value
        """
        ...

    def fuzz(self) -> _T: ...

class FuzzyText(BaseFuzzyAttribute):
    """
    Generate random text strings.

    Example:
        code = factory.FuzzyText(length=10)
        token = factory.FuzzyText(prefix='TOKEN_', length=20)
        hex_value = factory.FuzzyText(length=8, chars='0123456789ABCDEF')
    """
    prefix: str
    suffix: str
    length: int
    chars: tuple[str, ...]

    def __init__(
        self,
        prefix: str = '',
        length: int = 12,
        suffix: str = '',
        chars: str | Sequence[str] = ...  # Default: string.ascii_letters
    ) -> None:
        """
        Initialize a fuzzy text generator.

        Args:
            prefix: String to prepend to the generated text
            length: Length of the random part
            suffix: String to append to the generated text
            chars: Characters to choose from
        """
        ...

    def fuzz(self) -> str: ...

class FuzzyChoice(BaseFuzzyAttribute):
    """
    Randomly choose from a list of options.

    Example:
        status = factory.FuzzyChoice(['pending', 'active', 'closed'])
        user = factory.FuzzyChoice(User.objects.all())
        priority = factory.FuzzyChoice([1, 2, 3], getter=lambda x: x * 10)
    """
    choices: list[_T] | None
    choices_generator: Iterable[_T]
    getter: Callable[[Any], _T] | None

    def __init__(
        self,
        choices: Iterable[_T],
        getter: Callable[[Any], _T] | None = None
    ) -> None:
        """
        Initialize with choices.

        Args:
            choices: An iterable of choices (will be unrolled on first use)
            getter: Optional function to transform the chosen value
        """
        ...

    def fuzz(self) -> _T: ...

class FuzzyInteger(BaseFuzzyAttribute):
    """
    Generate random integers within a range.

    Example:
        age = factory.FuzzyInteger(18, 100)
        count = factory.FuzzyInteger(50)  # 0-50
        even_number = factory.FuzzyInteger(0, 100, step=2)
    """
    low: int
    high: int
    step: int

    def __init__(self, low: int, high: int | None = None, step: int = 1) -> None:
        """
        Initialize a fuzzy integer generator.

        Args:
            low: Lower bound (inclusive), or upper bound if high is None
            high: Upper bound (inclusive)
            step: Step between values (default: 1)
        """
        ...

    def fuzz(self) -> int: ...

class FuzzyDecimal(BaseFuzzyAttribute):
    """
    Generate random decimal numbers within a range.

    Example:
        price = factory.FuzzyDecimal(0.99, 999.99)
        precise_value = factory.FuzzyDecimal(0, 1, precision=5)
    """
    low: float
    high: float
    precision: int

    def __init__(
        self,
        low: float,
        high: float | None = None,
        precision: int = 2
    ) -> None:
        """
        Initialize a fuzzy decimal generator.

        Args:
            low: Lower bound, or upper bound if high is None
            high: Upper bound
            precision: Number of decimal places
        """
        ...

    def fuzz(self) -> decimal.Decimal: ...

class FuzzyFloat(BaseFuzzyAttribute):
    """
    Generate random floats within a range.

    Example:
        temperature = factory.FuzzyFloat(-40.0, 50.0)
        percentage = factory.FuzzyFloat(0, 100, precision=2)
    """
    low: float
    high: float
    precision: int

    def __init__(
        self,
        low: float,
        high: float | None = None,
        precision: int = 15
    ) -> None:
        """
        Initialize a fuzzy float generator.

        Args:
            low: Lower bound, or upper bound if high is None
            high: Upper bound
            precision: Number of significant digits
        """
        ...

    def fuzz(self) -> float: ...

class FuzzyDate(BaseFuzzyAttribute):
    """
    Generate random dates within a range.

    Example:
        import datetime
        birth_date = factory.FuzzyDate(
            datetime.date(1950, 1, 1),
            datetime.date(2000, 12, 31)
        )
        # With default end date (today):
        recent_date = factory.FuzzyDate(datetime.date(2020, 1, 1))
    """
    start_date: int  # ordinal
    end_date: int  # ordinal

    def __init__(
        self,
        start_date: datetime.date,
        end_date: datetime.date | None = None
    ) -> None:
        """
        Initialize a fuzzy date generator.

        Args:
            start_date: Start of date range
            end_date: End of date range (default: today)
        """
        ...

    def fuzz(self) -> datetime.date: ...

class BaseFuzzyDateTime(BaseFuzzyAttribute):
    """
    Base class for fuzzy datetime generators.

    Provides the ability to force specific components (year, month, etc.).
    """
    start_dt: datetime.datetime
    end_dt: datetime.datetime
    force_year: int | None
    force_month: int | None
    force_day: int | None
    force_hour: int | None
    force_minute: int | None
    force_second: int | None
    force_microsecond: int | None

    def _check_bounds(
        self,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime
    ) -> None: ...

    def _now(self) -> datetime.datetime:
        """Get the current datetime (implemented by subclasses)."""
        ...

    def __init__(
        self,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime | None = None,
        force_year: int | None = None,
        force_month: int | None = None,
        force_day: int | None = None,
        force_hour: int | None = None,
        force_minute: int | None = None,
        force_second: int | None = None,
        force_microsecond: int | None = None
    ) -> None:
        """
        Initialize a fuzzy datetime generator.

        Args:
            start_dt: Start of datetime range
            end_dt: End of datetime range (default: now)
            force_year: Force a specific year
            force_month: Force a specific month
            force_day: Force a specific day
            force_hour: Force a specific hour
            force_minute: Force a specific minute
            force_second: Force a specific second
            force_microsecond: Force a specific microsecond
        """
        ...

    def fuzz(self) -> datetime.datetime: ...

class FuzzyNaiveDateTime(BaseFuzzyDateTime):
    """
    Generate random naive (timezone-unaware) datetimes.

    Example:
        import datetime
        created_at = factory.FuzzyNaiveDateTime(
            datetime.datetime(2020, 1, 1, 0, 0, 0)
        )
        # Force specific time components:
        same_day = factory.FuzzyNaiveDateTime(
            datetime.datetime(2020, 1, 1),
            force_hour=9,
            force_minute=0
        )
    """
    def _now(self) -> datetime.datetime: ...

    def _check_bounds(
        self,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime
    ) -> None: ...

class FuzzyDateTime(BaseFuzzyDateTime):
    """
    Generate random timezone-aware datetimes.

    Example:
        import datetime
        created_at = factory.FuzzyDateTime(
            datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        )
    """
    def _now(self) -> datetime.datetime: ...

    def _check_bounds(
        self,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime
    ) -> None: ...
