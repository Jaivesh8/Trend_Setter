# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### 1. Initialize and Search

```python
from search_engine import SearchEngine

# Initialize (loads ChromaDB and PKL files)
engine = SearchEngine()

# Search
results = engine.search("your query", top_k=10)

# Access results
for result in results['results']:
    print(f"ID: {result['id']}")
    print(f"Distance: {result['chroma']['distance']}")
    print(f"Document: {result['chroma']['document']}")
    
    # Access PKL data if available
    if 'text_pkl' in result:
        print(f"Text embedding available")
    if 'image_pkl' in result:
        print(f"Image embedding available")
```

### 2. Get Documents by IDs

```python
# Get specific documents
data = engine.get_by_ids(["id1", "id2", "id3"])

# Access ChromaDB data
chroma_data = data['chroma']

# Access PKL data
text_data = data['text_pkl']
image_data = data['image_pkl']
```

### 3. Create ID Mapping

```python
# Map all IDs across sources
mapping = engine.create_id_mapping()

# Check where an ID exists
doc_id = "some_id"
if doc_id in mapping:
    print(f"In ChromaDB: {mapping[doc_id].get('chroma', False)}")
    print(f"In Text PKL: {mapping[doc_id].get('text_pkl', False)}")
    print(f"In Image PKL: {mapping[doc_id].get('image_pkl', False)}")
```

### 4. Command Line Usage

```bash
# Search
python main.py search "your query"

# Get info
python main.py info

# Get by IDs
python main.py get-by-ids id1 id2

# Create mapping
python main.py map-ids

# JSON output
python main.py search "query" --json
```

## Process Flow

1. **Initialization**
   - Load ChromaDB collections
   - Load text_embeddings.pkl
   - Load image_embeddings.pkl
   - Create mapper connections

2. **Search Process**
   - Query ChromaDB with text or embeddings
   - Get matching document IDs
   - Map IDs to PKL files
   - Combine results into unified format

3. **Mapping Process**
   - Extract IDs from ChromaDB results
   - Lookup IDs in PKL files
   - Combine data from all sources
   - Return unified or separate formats

## Key Components

- **ChromaManager**: Handles ChromaDB operations
- **PKLLoader**: Manages PKL file loading and access
- **DataMapper**: Maps between ChromaDB and PKL data
- **SearchEngine**: Unified interface for all operations

## Result Formats

### Unified Format (default)
```python
{
    "query": "search text",
    "total_results": 10,
    "results": [
        {
            "id": "doc_id",
            "chroma": {
                "distance": 0.5,
                "metadata": {...},
                "document": "text content"
            },
            "text_pkl": {
                "embedding": [...],
                "metadata": {...},
                "document": "text"
            },
            "image_pkl": {
                "embedding": [...],
                "metadata": {...},
                "document": "image data"
            }
        }
    ]
}
```

### Separate Format
```python
{
    "query": "search text",
    "chroma": {...},
    "text_pkl": {...},
    "image_pkl": {...},
    "mapped_ids": [...]
}
```
