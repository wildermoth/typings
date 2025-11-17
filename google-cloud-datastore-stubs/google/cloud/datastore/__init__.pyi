"""Type stubs for google.cloud.datastore"""

# Submodules - allows access like datastore.query.PropertyFilter
from google.cloud.datastore import aggregation as aggregation
from google.cloud.datastore import batch as batch
from google.cloud.datastore import client as client
from google.cloud.datastore import entity as entity
from google.cloud.datastore import helpers as helpers
from google.cloud.datastore import key as key
from google.cloud.datastore import query as query
from google.cloud.datastore import query_profile as query_profile
from google.cloud.datastore import transaction as transaction

# Main exports
from google.cloud.datastore.batch import Batch as Batch
from google.cloud.datastore.client import Client as Client
from google.cloud.datastore.entity import Entity as Entity
from google.cloud.datastore.key import Key as Key
from google.cloud.datastore.query import Query as Query
from google.cloud.datastore.query_profile import ExplainOptions as ExplainOptions
from google.cloud.datastore.transaction import Transaction as Transaction
from google.cloud.datastore.version import __version__ as __version__

__all__ = [
    "__version__",
    "Batch",
    "Client",
    "Entity",
    "Key",
    "Query",
    "ExplainOptions",
    "Transaction",
    "aggregation",
    "batch",
    "client",
    "entity",
    "helpers",
    "key",
    "query",
    "query_profile",
    "transaction",
]
