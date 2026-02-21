"""
DEMO: See exactly what the code does step by step
"""
from search_engine import SearchEngine

print("=" * 60)
print("STEP 1: Import SearchEngine")
print("=" * 60)
print("from search_engine import SearchEngine")
print("✓ Imported successfully!\n")

print("=" * 60)
print("STEP 2: Create SearchEngine instance")
print("=" * 60)
print("engine = SearchEngine()")
print("This will:")
print("  - Connect to ChromaDB")
print("  - Load text_embeddings.pkl")
print("  - Load image_embeddings.pkl")
print("  - Set up mapping connections\n")

engine = SearchEngine()

print("\n" + "=" * 60)
print("STEP 3: Search for something")
print("=" * 60)
print('results = engine.search("photography", top_k=3)')
print("This will:")
print("  - Search ChromaDB for 'photography'")
print("  - Get top 3 most similar results")
print("  - Map results to PKL files")
print("  - Return unified results\n")

results = engine.search("photography", top_k=3)

print("\n" + "=" * 60)
print("STEP 4: What you got back")
print("=" * 60)
print(f"Query: {results['query']}")
print(f"Total Results: {results['total_results']}")
print(f"Number of result objects: {len(results['results'])}\n")

print("=" * 60)
print("STEP 5: Access the results")
print("=" * 60)
for i, result in enumerate(results['results'], 1):
    print(f"\n--- Result {i} ---")
    print(f"ID: {result['id']}")
    print(f"Text (first 150 chars): {result['chroma']['document'][:150]}...")
    print(f"Distance (lower = more similar): {result['chroma']['distance']:.4f}")
    
    # Show what data is available
    available = []
    if 'text_pkl' in result:
        available.append("Text PKL")
    if 'image_pkl' in result:
        available.append("Image PKL")
    print(f"Available data: {', '.join(available) if available else 'ChromaDB only'}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
The code does this:
1. Import → Gets the SearchEngine class
2. Create → Loads all your data (ChromaDB + PKL files)
3. Search → Finds similar transcripts and maps to PKL data
4. Use → Access results with result['id'], result['chroma']['document'], etc.

You can now search your transcripts and get mapped results!
""")
