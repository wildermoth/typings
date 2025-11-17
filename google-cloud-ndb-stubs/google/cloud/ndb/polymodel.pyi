"""Type stubs for google.cloud.ndb.polymodel"""

from google.cloud.ndb import model

class PolyModel(model.Model):
    """Model class that supports polymorphic hierarchies."""

    class_: list[str]

    @classmethod
    def _get_kind(cls) -> str: ...

    @classmethod
    def _class_name(cls) -> str: ...

    @classmethod
    def _class_key(cls) -> list[str]: ...
