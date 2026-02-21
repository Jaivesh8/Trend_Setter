# Code Explanation: How SearchEngine Works

## The Code Breakdown

```python
from search_engine import SearchEngine
engine = SearchEngine()
results = engine.search("your query", top_k=10)
```

### Line 1: `from search_engine import SearchEngine`
**What it does:**
- Imports the `SearchEngine` class from the `search_engine.py` file
- This gives you access to all the search functionality

**Think of it like:** Getting a tool from a toolbox

---

### Line 2: `engine = SearchEngine()`
**What it does:**
- Creates a new instance of SearchEngine
- **Automatically loads everything:**
  - ✅ Connects to ChromaDB (your transcript database)
  - ✅ Loads `text_embeddings.pkl` file
  - ✅ Loads `image_embeddings.pkl` file
  - ✅ Sets up all connections for searching and mapping

**Think of it like:** Starting up your car - it loads all systems

**What you'll see:**
```
Initializing Search Engine...
Loaded 2 collection(s) from ChromaDB
Loaded text embeddings: 1134 items
Loaded image embeddings: 1123 items
Search Engine initialized successfully!
```

---

### Line 3: `results = engine.search("your query", top_k=10)`
**What it does:**
- Searches your ChromaDB for transcripts similar to "your query"
- Gets the top 10 most similar results
- **Automatically maps** those results to your PKL files
- Returns everything in one unified format

**Parameters:**
- `"your query"` - The text you want to search for
- `top_k=10` - How many results you want (default is 10)

**Think of it like:** Asking Google a question and getting 10 best answers

---

## What You Get Back

The `results` variable contains:

```python
{
    "query": "your query",
    "total_results": 10,
    "results": [
        {
            "id": "document_id_123",
            "chroma": {
                "distance": 0.5,        # Lower = more similar
                "document": "Full text...",
                "metadata": {...}
            },
            "text_pkl": {              # If available
                "embedding": [...],
                "metadata": {...}
            },
            "image_pkl": {             # If available
                "embedding": [...],
                "metadata": {...}
            }
        },
        # ... 9 more results
    ]
}
```

---

## Real Example

```python
from search_engine import SearchEngine

# Step 1: Create engine (loads everything)
engine = SearchEngine()

# Step 2: Search
results = engine.search("photography", top_k=5)

# Step 3: Use results
print(f"Found {results['total_results']} results")

for result in results['results']:
    print(f"ID: {result['id']}")
    print(f"Text: {result['chroma']['document']}")
    print(f"Similarity: {1 - result['chroma']['distance']:.2f}")
```

**Output:**
```
Found 5 results
ID: 3172793078973376764
Text: Photography, A realm of boundless perspectives 📸...
Similarity: 0.67
```

---

## Complete Working Example

```python
from search_engine import SearchEngine

# Initialize (do this once, reuse the engine)
engine = SearchEngine()

# Search for something
results = engine.search("college event", top_k=3)

# Process results
for i, result in enumerate(results['results'], 1):
    print(f"\n--- Result {i} ---")
    print(f"ID: {result['id']}")
    print(f"Text: {result['chroma']['document'][:200]}...")
    
    # Check if PKL data exists
    if 'text_pkl' in result:
        print("✓ Has text embedding")
    if 'image_pkl' in result:
        print("✓ Has image embedding")
```

---

## Key Points

1. **Import once** - `from search_engine import SearchEngine`
2. **Create engine once** - `engine = SearchEngine()` (takes a few seconds to load)
3. **Reuse the engine** - Don't create a new engine for each search
4. **Search many times** - `engine.search("query1")`, `engine.search("query2")`, etc.

---

## Other Useful Methods

```python
engine = SearchEngine()

# Get documents by specific IDs
data = engine.get_by_ids(["id1", "id2", "id3"])

# Get system information
info = engine.get_collection_info()

# Create ID mapping
mapping = engine.create_id_mapping()
```
