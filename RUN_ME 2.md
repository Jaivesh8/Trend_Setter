# 🚀 System is Ready! Here's How to Use It

## ✅ Status: WORKING
- ✅ Dependencies installed
- ✅ ChromaDB connected (2 collections: reel_images, reel_text)
- ✅ Text embeddings loaded: 1,134 items
- ✅ Image embeddings loaded: 1,123 items

## Quick Start

### 1. Command Line Usage

```bash
# Get system info
python3 main.py info

# Search transcripts
python3 main.py search "your search query here"

# Search with more results
python3 main.py search "your query" --top-k 20

# Get documents by IDs
python3 main.py get-by-ids id1 id2 id3

# Create ID mapping
python3 main.py map-ids

# JSON output
python3 main.py search "query" --json
```

### 2. Python Code Usage

```python
from search_engine import SearchEngine

# Initialize (loads everything)
engine = SearchEngine()

# Search
results = engine.search("your query", top_k=10)

# Use results
for result in results['results']:
    print(f"ID: {result['id']}")
    print(f"Text: {result['chroma']['document']}")
    print(f"Distance: {result['chroma']['distance']}")
    if 'text_pkl' in result:
        print("Has text embedding")
    if 'image_pkl' in result:
        print("Has image embedding")
```

### 3. Run Examples

```bash
# Simple example
python3 simple_example.py

# Detailed examples
python3 how_to_use.py
```

## What It Does

1. **Searches ChromaDB** - Finds similar transcripts
2. **Maps to PKL Files** - Automatically links results to your vectorized data
3. **Returns Unified Results** - Combines data from all sources

## Your Data

- **ChromaDB Collections**: reel_images (1,123 docs), reel_text
- **Text PKL**: 1,134 embeddings
- **Image PKL**: 1,123 embeddings

## Next Steps

Try these commands:
```bash
python3 main.py info
python3 main.py search "machine learning"
python3 simple_example.py
```

Everything is ready to use! 🎉
