# Google Cloud Datastore & NDB Type Stubs

This repository contains comprehensive type stubs (`.pyi` files) for the `google-cloud-datastore` and `google-cloud-ndb` libraries to enable better type checking and IDE support.

## Installation

To use these type stubs with your LSP, you can add them to your project's Python path or install them as a package.

### Option 1: Add to Python Path

Add the `google-cloud-datastore-stubs` directory to your PYTHONPATH or place it in your project directory.

### Option 2: Local Installation

For Datastore:
```bash
pip install -e google-cloud-datastore-stubs/
```

For NDB:
```bash
pip install -e google-cloud-ndb-stubs/
```

## Usage

Once installed, your LSP (Language Server Protocol) and type checkers like mypy will automatically discover and use these type stubs when working with the `google-cloud-datastore` library.

## Coverage

### google-cloud-datastore stubs cover:

- `google.cloud.datastore` - Main module with exports
- `google.cloud.datastore.client` - Client class for Datastore operations
- `google.cloud.datastore.entity` - Entity class representing datastore rows
- `google.cloud.datastore.key` - Key class for entity identification
- `google.cloud.datastore.query` - Query classes for data retrieval
- `google.cloud.datastore.aggregation` - Aggregation query support
- `google.cloud.datastore.batch` - Batch operations
- `google.cloud.datastore.transaction` - Transaction support
- `google.cloud.datastore.helpers` - Helper functions and GeoPoint class
- `google.cloud.datastore.query_profile` - Query profiling and explain options

### google-cloud-ndb stubs cover:

- `google.cloud.ndb` - Main NDB module with all exports
- `google.cloud.ndb.model` - Model class and all Property types (StringProperty, IntegerProperty, etc.)
- `google.cloud.ndb.key` - Key class for entity identification
- `google.cloud.ndb.query` - Query classes and filter operations
- `google.cloud.ndb.context` - Context management for NDB operations
- `google.cloud.ndb.tasklets` - Async tasklet support with Futures
- `google.cloud.ndb.client` - NDB Client class
- `google.cloud.ndb.exceptions` - NDB exception types
- `google.cloud.ndb.polymodel` - Polymorphic model support
- `google.cloud.ndb.global_cache` - Memcache and Redis cache implementations

## Examples

### Datastore Example

```python
from google.cloud import datastore

# Your LSP will now provide full type hints and autocompletion
client = datastore.Client()
key = client.key('Task', 'sampleTask')
entity = datastore.Entity(key=key)
entity['description'] = 'Buy milk'
client.put(entity)

# Query with type hints
query = client.query(kind='Task')
results = list(query.fetch())
```

### NDB Example

```python
from google.cloud import ndb

# Define a model with full type support
class Task(ndb.Model):
    description = ndb.StringProperty()
    completed = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)

# Your LSP now understands Model.key, _get_kind(), and all properties
client = ndb.Client()
with client.context():
    # Create and save
    task = Task(description='Buy milk')
    task.put()

    # Query with type hints
    query = Task.query(Task.completed == False)
    tasks = query.fetch()

    # Get kind
    kind = Task._get_kind()  # Now typed correctly
```

## Compatibility

- `google-cloud-datastore` stubs are compatible with version 2.21.0 and similar versions
- `google-cloud-ndb` stubs are compatible with version 2.3.4 and similar versions

## Contributing

If you find any issues or missing type annotations, feel free to submit a pull request or open an issue.

## License

These type stubs follow the same Apache 2.0 license as the `google-cloud-datastore` and `google-cloud-ndb` libraries.
