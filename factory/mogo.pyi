"""
Type stubs for factory.mogo module.

Mogo (pymongo wrapper) integration for factory_boy.
"""

from typing import Any, TypeVar
from . import base

_T = TypeVar('_T')

class MogoFactory(base.Factory[_T]):
    """
    Factory for Mogo models.

    Example:
        from mogo import Model, Field

        class User(Model):
            username = Field(str)
            email = Field(str)

        class UserFactory(factory.mogo.MogoFactory):
            class Meta:
                model = User

            username = factory.Sequence(lambda n: f'user{n}')
            email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    """
    class Meta:
        abstract: bool  # True

    @classmethod
    def _build(cls, model_class: type[_T], *args: Any, **kwargs: Any) -> _T:
        """
        Build a Mogo model without saving.

        Args:
            model_class: The model class
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            The model instance (not saved)
        """
        ...

    @classmethod
    def _create(cls, model_class: type[_T], *args: Any, **kwargs: Any) -> _T:
        """
        Create and save a Mogo model.

        Args:
            model_class: The model class
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            The saved model instance
        """
        ...
