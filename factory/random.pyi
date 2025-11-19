"""
Type stubs for factory.random module.

Random state management for factory_boy and faker integration.
"""

import random as _random
from typing import Any

# Global random generator used by factory.fuzzy
randgen: _random.Random

def get_random_state() -> tuple[Any, ...]:
    """
    Retrieve the current state of factory.fuzzy's random generator.

    The returned state represents both Faker and factory_boy random generators,
    which are kept in sync.

    Returns:
        The random state (suitable for passing to set_random_state)
    """
    ...

def set_random_state(state: tuple[Any, ...]) -> None:
    """
    Force-set the state of factory.fuzzy's random generator.

    This also updates Faker's random generator to maintain synchronization.

    Args:
        state: The state to set (typically from get_random_state)
    """
    ...

def reseed_random(seed: int) -> None:
    """
    Reseed factory.fuzzy's random generator with a specific seed.

    This ensures reproducible random values in tests.

    Args:
        seed: The random seed to use
    """
    ...
