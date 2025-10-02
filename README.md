# easySaveClient

`easySaveClient` is a Python client library for interacting with the EasySave API. It provides a high-level interface for performing CRUD (Create, Read, Update, Delete) operations on data blocks using a simple and intuitive design.

## Features

- Authenticate with EasySave API using username and password.
- Create new data blocks using string or typed inputs.
- Retrieve blocks with flexible filtering.
- Update or delete existing blocks.
- Serialize and deserialize blocks easily.


## Installation

```bash
pip install easysaveservice
```

## Getting Started

### Importing the service

```python
import easysave
```

### Configuring client

```python
es = easysave.easySaveClient("USERNAME", "PASSWORD")
```

## Basic Usage

### Retrieve data block/s

```python
blocks = es.getBlocks("name")
```

You can retrieve all blocks that match the following pattern: *name**. This means any value starting with *name* will be retrieved in the form of a list.

```python
block = es.getBlocks("name", strict=True)
```

Setting **strict=True** will ensure only the block which exactly matches *name* will be retrieved.

The above functions return a list of dictionaries in the following format:

```json
{"identifier": identifier, "value": value}
```

If you wish to retrieve a list of blocks using the easysave.Block class, use the following alteration of the function:

```python
es.getBlocksTyped(identifier)
```

### Creating data block

```python
es.createBlock("identifier", "value")
```

Alternative, you can use the typed version:

```python
es.createBlockTyped(BlockInstance)
```

### Altering data block

```python
es.updateBlock("identifier", "newvalue")
```

### Deleting data block

```python
es.deleteBlock("identifier")
```