"""
Type stubs for factory.django module.

Django ORM integration for factory_boy.
"""

from typing import Any, Callable, ClassVar, Dict, Sequence, Type, TypeVar
from django.db.models import Model, Manager
from django.core.files import File
from . import base, declarations

_T = TypeVar('_T')
_M = TypeVar('_M', bound=Model)

DEFAULT_DB_ALIAS: str  # 'default'

def get_model(app: str, model: str) -> Type[Model]:
    """
    Get a Django model class by app and model name.

    Args:
        app: The app label
        model: The model name

    Returns:
        The model class
    """
    ...

class DjangoOptions(base.FactoryOptions):
    """
    FactoryOptions subclass with Django-specific options.

    Additional Meta options:
        django_get_or_create: Tuple of field names for get_or_create
        database: Database alias to use (default: 'default')
        skip_postgeneration_save: Skip saving after post-generation (default: False)
    """
    django_get_or_create: Sequence[str]
    database: str
    skip_postgeneration_save: bool

    def _build_default_options(self) -> list[base.OptionDefault]: ...

    def _get_counter_reference(self) -> base.FactoryOptions: ...

    def get_model_class(self) -> Type[Model] | None: ...

class DjangoModelFactory(base.Factory[_M]):
    """
    Factory for Django models.

    Example:
        from django.contrib.auth.models import User

        class UserFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = User
                # Or by string reference:
                # model = 'auth.User'

            username = factory.Sequence(lambda n: f'user{n}')
            email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

        # With get_or_create:
        class GroupFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = 'auth.Group'
                django_get_or_create = ('name',)

            name = 'admins'
    """
    _options_class: ClassVar[Type[DjangoOptions]]
    _original_params: Dict[str, Any] | None

    class Meta:
        abstract: bool  # True

    @classmethod
    def _load_model_class(cls, definition: Type[_M] | str) -> Type[_M]:
        """
        Load a model class from a string reference or return the class.

        Args:
            definition: Model class or 'app.Model' string

        Returns:
            The model class
        """
        ...

    @classmethod
    def _get_manager(cls, model_class: Type[_M]) -> Manager[_M]:
        """
        Get the manager for the model.

        Args:
            model_class: The model class

        Returns:
            The model's manager (using the configured database)
        """
        ...

    @classmethod
    def _generate(cls, strategy: str, params: Dict[str, Any]) -> _M: ...

    @classmethod
    def _get_or_create(cls, model_class: Type[_M], *args: Any, **kwargs: Any) -> _M:
        """
        Get or create an instance using django_get_or_create fields.

        Args:
            model_class: The model class
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            The model instance
        """
        ...

    @classmethod
    def _create(cls, model_class: Type[_M], *args: Any, **kwargs: Any) -> _M: ...

    @classmethod
    def _after_postgeneration(
        cls,
        instance: _M,
        create: bool,
        results: Dict[str, Any] | None = None
    ) -> None: ...

class Password(declarations.Transformer):
    """
    Transform a plain password into a hashed password using Django's make_password.

    Example:
        class UserFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = User

            password = factory.django.Password('defaultpassword')

        # Usage:
        user = UserFactory()  # password is hashed
        user = UserFactory(password='custom')  # custom password is hashed
        user = UserFactory(password=Password.Force('plain'))  # keeps 'plain' unhashed
    """
    def __init__(
        self,
        password: Any,
        transform: Callable[[Any], str] = ...,  # Default: django.contrib.auth.hashers.make_password
        **kwargs: Any
    ) -> None: ...

class FileField(declarations.BaseDeclaration):
    """
    Generate Django FileField values.

    Example:
        class DocumentFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Document

            # From raw data:
            file = factory.django.FileField(data=b'file contents')

            # From a file path:
            file = factory.django.FileField(from_path='/path/to/file.pdf')

            # From a file object:
            file = factory.django.FileField(from_file=open('/path/to/file.pdf', 'rb'))

            # From a function:
            file = factory.django.FileField(from_func=lambda: open('/tmp/file.txt', 'rb'))

            # With custom filename:
            file = factory.django.FileField(filename='custom.txt', data=b'contents')
    """
    DEFAULT_FILENAME: ClassVar[str]  # 'example.dat'

    def _make_data(self, params: Dict[str, Any]) -> bytes:
        """Generate the file data."""
        ...

    def _make_content(self, params: Dict[str, Any]) -> tuple[str, File]:
        """
        Generate the file content and filename.

        Returns:
            Tuple of (filename, content)
        """
        ...

    def evaluate(
        self,
        instance: Any,
        step: Any,
        extra: Dict[str, Any]
    ) -> File: ...

class ImageField(FileField):
    """
    Generate Django ImageField values.

    Requires Pillow to be installed.

    Example:
        class ProfileFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = Profile

            avatar = factory.django.ImageField(color='blue')
            avatar = factory.django.ImageField(width=1920, height=1080)
            avatar = factory.django.ImageField(
                color='red',
                width=200,
                height=200,
                format='PNG'
            )
    """
    DEFAULT_FILENAME: ClassVar[str]  # 'example.jpg'

    def _make_data(self, params: Dict[str, Any]) -> bytes:
        """
        Generate image data.

        Params:
            width: Image width (default: 100)
            height: Image height (default: width)
            color: Image color (default: 'blue')
            format: Image format (default: 'JPEG')
            palette: Color palette (default: 'RGB')
        """
        ...

class mute_signals:
    """
    Temporarily disable and restore Django signals.

    Can be used as a context manager or decorator.

    Example:
        from django.db.models.signals import pre_save, post_save

        # As context manager:
        with factory.django.mute_signals(pre_save, post_save):
            user = UserFactory()

        # As class decorator:
        @factory.django.mute_signals(post_save)
        class UserFactory(factory.django.DjangoModelFactory):
            class Meta:
                model = User

        # As function decorator:
        @factory.django.mute_signals(post_save)
        def create_users():
            return UserFactory.create_batch(10)
    """
    signals: tuple[Any, ...]
    paused: Dict[Any, list[Any]]

    def __init__(self, *signals: Any) -> None:
        """
        Initialize with signals to mute.

        Args:
            *signals: Django signals to disable
        """
        ...

    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None: ...

    def copy(self) -> mute_signals:
        """Create a copy of this mute_signals instance."""
        ...

    def __call__(self, callable_obj: _T) -> _T:
        """
        Use as a decorator on factories or functions.

        Args:
            callable_obj: Factory class or function to wrap

        Returns:
            Wrapped object
        """
        ...

    def wrap_method(self, method: Callable[..., _T]) -> Callable[..., _T]:
        """Wrap a method to mute signals."""
        ...
