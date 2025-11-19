"""
Type stubs for factory.enums module.

Constants and enumerations used throughout factory_boy.
"""

from typing import Any, Optional

# Build strategies
BUILD_STRATEGY: str  # 'build'
CREATE_STRATEGY: str  # 'create'
STUB_STRATEGY: str  # 'stub'

# String for splitting attribute names into (subfactory_name, subfactory_field) tuples
SPLITTER: str  # '__'

class BuilderPhase:
    """
    Enumeration of builder phases for declarations.

    Declarations can be evaluated at different phases:
    - ATTRIBUTE_RESOLUTION: during attribute computation
    - POST_INSTANTIATION: after the target object has been built
    """
    ATTRIBUTE_RESOLUTION: str  # 'attributes'
    POST_INSTANTIATION: str  # 'post_instance'

def get_builder_phase(obj: Any) -> Optional[str]:
    """
    Get the builder phase for an object.

    Args:
        obj: The object to check

    Returns:
        The builder phase (ATTRIBUTE_RESOLUTION or POST_INSTANTIATION) or None
    """
    ...
