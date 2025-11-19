"""
Type stubs for factory.faker module.

Integration with the Faker library for generating fake data.
"""

from typing import Any, ContextManager, Dict
from faker import Faker as FakerGenerator
from . import builder, declarations

class Faker(declarations.BaseDeclaration):
    """
    Wrapper for Faker provider values.

    Example:
        class UserFactory(factory.Factory):
            class Meta:
                model = User

            first_name = factory.Faker('first_name')
            last_name = factory.Faker('last_name')
            email = factory.Faker('email')
            # With locale:
            name_fr = factory.Faker('name', locale='fr_FR')
            # With provider arguments:
            ean13 = factory.Faker('ean', length=13)
    """
    provider: str
    _FAKER_REGISTRY: Dict[str, FakerGenerator]
    _DEFAULT_LOCALE: str

    def __init__(self, provider: str, **kwargs: Any) -> None:
        """
        Initialize a Faker declaration.

        Args:
            provider: The name of the Faker provider method (e.g., 'name', 'email')
            locale: Optional locale to use (e.g., 'en_US', 'fr_FR')
            **kwargs: Additional keyword arguments for the provider
        """
        ...

    def evaluate(
        self,
        instance: Any,
        step: builder.BuildStep,
        extra: Dict[str, Any]
    ) -> Any: ...

    @classmethod
    def override_default_locale(cls, locale: str) -> ContextManager[None]:
        """
        Context manager to temporarily override the default locale.

        Example:
            with factory.Faker.override_default_locale('fr_FR'):
                user = UserFactory()  # Uses French locale

        Args:
            locale: The locale to use

        Returns:
            Context manager
        """
        ...

    @classmethod
    def _get_faker(cls, locale: str | None = None) -> FakerGenerator:
        """
        Get a Faker instance for the specified locale.

        Args:
            locale: The locale (or None for default)

        Returns:
            A Faker generator instance
        """
        ...

    @classmethod
    def add_provider(cls, provider: Any, locale: str | None = None) -> None:
        """
        Add a custom Faker provider for the specified locale.

        Example:
            from faker.providers import BaseProvider

            class MyProvider(BaseProvider):
                def custom_value(self):
                    return 'custom'

            factory.Faker.add_provider(MyProvider)

        Args:
            provider: The provider class to add
            locale: Optional specific locale
        """
        ...
