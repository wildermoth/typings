"""
Type stubs for factory.mongoengine module.

MongoEngine ORM integration for factory_boy.
"""

from typing import Any, TypeVar
from . import base

_T = TypeVar('_T')

class MongoEngineFactory(base.Factory[_T]):
    """
    Factory for MongoEngine documents.

    Example:
        from mongoengine import Document, StringField, connect

        connect('test_db')

        class User(Document):
            username = StringField(required=True)
            email = StringField(required=True)

        class UserFactory(factory.mongoengine.MongoEngineFactory):
            class Meta:
                model = User

            username = factory.Sequence(lambda n: f'user{n}')
            email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

        # Usage:
        user = UserFactory()  # Creates and saves to MongoDB
        user = UserFactory.build()  # Creates without saving
    """
    class Meta:
        abstract: bool  # True

    @classmethod
    def _build(cls, model_class: type[_T], *args: Any, **kwargs: Any) -> _T:
        """
        Build a MongoEngine document without saving.

        Args:
            model_class: The document class
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            The document instance (not saved)
        """
        ...

    @classmethod
    def _create(cls, model_class: type[_T], *args: Any, **kwargs: Any) -> _T:
        """
        Create and save a MongoEngine document.

        Args:
            model_class: The document class
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            The saved document instance
        """
        ...
