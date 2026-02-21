"""
Example: How to use SearchEngine in your code
"""
from search_engine import SearchEngine

# Step 1: Import SearchEngine class
# This brings in the main search engine class from search_engine.py

# Step 2: Create an instance (this loads ChromaDB and PKL files)
engine = SearchEngine()
# What happens here:
# - Connects to ChromaDB database
# - Loads text_embeddings.pkl file
# - Loads image_embeddings.pkl file
# - Sets up all the mapping connections

# Step 3: Search for something
results = engine.search("your query", top_k=10)
# What happens here:
# - Searches ChromaDB for transcripts similar to "your query"
# - Gets top 10 most similar results
# - Maps those results to your PKL files
# - Returns everything in a unified format

# Step 4: Use the results
print(f"Found {results['total_results']} results\n")

for i, result in enumerate(results['results'], 1):
    print(f"Result {i}:")
    print(f"  ID: {result['id']}")
    print(f"  Text: {result['chroma']['document'][:100]}...")  # First 100 chars
    print(f"  Similarity Score: {1 - result['chroma']['distance']:.3f}")  # Convert distance to similarity
    
    # Check if PKL data is available
    if 'text_pkl' in result:
        print(f"  ✓ Has text embedding in PKL")
    if 'image_pkl' in result:
        print(f"  ✓ Has image embedding in PKL")
    print()
