"""
SIMPLE EXAMPLE - Copy and paste this to get started quickly!
"""

# Step 1: Import
from search_engine import SearchEngine

# Step 2: Create engine (loads everything automatically)
engine = SearchEngine()

# Step 3: Search
results = engine.search("your search query here", top_k=5)

# Step 4: Use results
for result in results['results']:
    print(f"ID: {result['id']}")
    print(f"Text: {result['chroma']['document']}")
    print(f"Distance: {result['chroma']['distance']}")
    print("---")
