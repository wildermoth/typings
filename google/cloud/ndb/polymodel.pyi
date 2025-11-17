"""Type stubs for google.cloud.ndb.polymodel"""

from google.cloud.ndb import model

class PolyModel(model.Model):
    """Model class that supports polymorphic hierarchies.

    PolyModel allows you to create model subclasses that share a datastore kind
    but can be queried and instantiated with their specific subclass type.

    Example:
        class Animal(PolyModel):
            name = StringProperty()

        class Cat(Animal):
            meow = StringProperty()

        class Dog(Animal):
            bark = StringProperty()
    """

    class_: list[str]

    @classmethod
    def _get_kind(cls) -> str: ...

    @classmethod
    def _class_name(cls) -> str: ...

    @classmethod
    def _class_key(cls) -> list[str]: ...
