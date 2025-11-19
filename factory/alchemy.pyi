"""
Type stubs for factory.alchemy module.

SQLAlchemy ORM integration for factory_boy.
"""

from typing import Any, ClassVar, Dict, Sequence, Type, TypeVar, Callable
from sqlalchemy.orm import Session
from . import base

_T = TypeVar('_T')

# Session persistence modes
SESSION_PERSISTENCE_COMMIT: str  # 'commit'
SESSION_PERSISTENCE_FLUSH: str  # 'flush'
VALID_SESSION_PERSISTENCE_TYPES: list[str | None]

class SQLAlchemyOptions(base.FactoryOptions):
    """
    FactoryOptions subclass with SQLAlchemy-specific options.

    Additional Meta options:
        sqlalchemy_get_or_create: Tuple of field names for get_or_create behavior
        sqlalchemy_session: SQLAlchemy session to use
        sqlalchemy_session_factory: Factory function that returns a session
        sqlalchemy_session_persistence: How to persist ('commit', 'flush', or None)
    """
    sqlalchemy_get_or_create: Sequence[str]
    sqlalchemy_session: Session | None
    sqlalchemy_session_factory: Callable[[], Session] | None
    sqlalchemy_session_persistence: str | None

    def _check_sqlalchemy_session_persistence(self, meta: Any, value: str | None) -> None: ...

    @staticmethod
    def _check_has_sqlalchemy_session_set(meta: Any, value: Any) -> None: ...

    def _build_default_options(self) -> list[base.OptionDefault]: ...

class SQLAlchemyModelFactory(base.Factory[_T]):
    """
    Factory for SQLAlchemy models.

    Example:
        from sqlalchemy import create_engine, Column, Integer, String
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import scoped_session, sessionmaker

        Base = declarative_base()
        engine = create_engine('sqlite:///:memory:')
        Session = scoped_session(sessionmaker(bind=engine))

        class User(Base):
            __tablename__ = 'users'
            id = Column(Integer, primary_key=True)
            username = Column(String(50))
            email = Column(String(100))

        class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
            class Meta:
                model = User
                sqlalchemy_session = Session
                sqlalchemy_session_persistence = 'commit'

            username = factory.Sequence(lambda n: f'user{n}')
            email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

        # With get_or_create:
        class RoleFactory(factory.alchemy.SQLAlchemyModelFactory):
            class Meta:
                model = Role
                sqlalchemy_session = Session
                sqlalchemy_get_or_create = ('name',)

            name = 'admin'

        # With session factory:
        class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
            class Meta:
                model = Post
                sqlalchemy_session_factory = lambda: Session()
                sqlalchemy_session_persistence = 'flush'
    """
    _options_class: ClassVar[Type[SQLAlchemyOptions]]
    _original_params: Dict[str, Any] | None

    class Meta:
        abstract: bool  # True

    @classmethod
    def _generate(cls, strategy: str, params: Dict[str, Any]) -> _T: ...

    @classmethod
    def _get_or_create(
        cls,
        model_class: Type[_T],
        session: Session,
        args: tuple[Any, ...],
        kwargs: Dict[str, Any]
    ) -> _T:
        """
        Get or create using sqlalchemy_get_or_create fields.

        Args:
            model_class: The model class
            session: The SQLAlchemy session
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            The model instance
        """
        ...

    @classmethod
    def _create(cls, model_class: Type[_T], *args: Any, **kwargs: Any) -> _T: ...

    @classmethod
    def _save(
        cls,
        model_class: Type[_T],
        session: Session,
        args: tuple[Any, ...],
        kwargs: Dict[str, Any]
    ) -> _T:
        """
        Save the instance to the database.

        Args:
            model_class: The model class
            session: The SQLAlchemy session
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            The persisted instance
        """
        ...
