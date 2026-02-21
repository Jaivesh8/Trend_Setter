"""
HOW TO USE THE CODE - Practical Examples
==========================================

This file shows you exactly how to use the search and mapping system in your code.
"""

# ============================================================================
# STEP 1: Import the SearchEngine
# ============================================================================
from search_engine import SearchEngine

# ============================================================================
# STEP 2: Initialize the Engine (loads ChromaDB and PKL files)
# ============================================================================
print("Initializing Search Engine...")
engine = SearchEngine()
# This will automatically:
# - Connect to ChromaDB
# - Load text_embeddings.pkl
# - Load image_embeddings.pkl
# - Set up all mappings

# ============================================================================
# EXAMPLE 1: Basic Search (Most Common Use Case)
# ============================================================================
print("\n" + "="*60)
print("EXAMPLE 1: Basic Search")
print("="*60)

# Search for transcripts
results = engine.search(
    query="what is machine learning",  # Your search query
    top_k=5  # Get top 5 results
)

# Access the results
print(f"Found {results['total_results']} results")

# Loop through each result
for i, result in enumerate(results['results'], 1):
    print(f"\n--- Result {i} ---")
    print(f"Document ID: {result['id']}")
    
    # ChromaDB data (always available)
    chroma_data = result['chroma']
    print(f"Similarity Distance: {chroma_data['distance']}")  # Lower = more similar
    print(f"Transcript Text: {chroma_data['document']}")
    if chroma_data.get('metadata'):
        print(f"Metadata: {chroma_data['metadata']}")
    
    # PKL data (if available)
    if 'text_pkl' in result:
        print("✓ Has text embedding in PKL")
        text_embedding = result['text_pkl']['embedding']
        print(f"  Text embedding shape: {len(text_embedding) if text_embedding else 'N/A'}")
    
    if 'image_pkl' in result:
        print("✓ Has image embedding in PKL")
        image_embedding = result['image_pkl']['embedding']
        print(f"  Image embedding shape: {len(image_embedding) if image_embedding else 'N/A'}")

# ============================================================================
# EXAMPLE 2: Get Specific Documents by ID
# ============================================================================
print("\n" + "="*60)
print("EXAMPLE 2: Get Documents by ID")
print("="*60)

# If you know specific document IDs, retrieve them directly
document_ids = ["doc_1", "doc_2", "doc_3"]  # Replace with your actual IDs

# Get full data for these IDs
full_data = engine.get_by_ids(document_ids)

# Access ChromaDB data
print(f"ChromaDB documents: {len(full_data['chroma'].get('ids', []))}")
for doc_id, doc_text in zip(
    full_data['chroma'].get('ids', []),
    full_data['chroma'].get('documents', [])
):
    print(f"  ID: {doc_id}")
    print(f"  Text: {doc_text[:100]}...")

# Access Text PKL data
if full_data.get('text_pkl'):
    print(f"\nText PKL documents: {len(full_data['text_pkl'].get('ids', []))}")
    for doc_id in full_data['text_pkl'].get('ids', []):
        print(f"  ID: {doc_id}")

# Access Image PKL data
if full_data.get('image_pkl'):
    print(f"\nImage PKL documents: {len(full_data['image_pkl'].get('ids', []))}")
    for doc_id in full_data['image_pkl'].get('ids', []):
        print(f"  ID: {doc_id}")

# ============================================================================
# EXAMPLE 3: Search with Filters
# ============================================================================
print("\n" + "="*60)
print("EXAMPLE 3: Search with Metadata Filters")
print("="*60)

# Search with metadata filters (if your ChromaDB has metadata)
results = engine.search(
    query="your search query",
    top_k=10,
    filter_dict={
        "category": "transcript",  # Example: filter by category
        # "date": "2024-01-01",    # Example: filter by date
    }
)

print(f"Found {results['total_results']} filtered results")

# ============================================================================
# EXAMPLE 4: Search Only Text or Only Image PKL Data
# ============================================================================
print("\n" + "="*60)
print("EXAMPLE 4: Selective PKL Data")
print("="*60)

# Search with only text PKL data (exclude image data)
results_text_only = engine.search(
    query="your query",
    top_k=5,
    include_text_pkl=True,   # Include text PKL
    include_image_pkl=False  # Exclude image PKL
)

# Search with only image PKL data (exclude text data)
results_image_only = engine.search(
    query="your query",
    top_k=5,
    include_text_pkl=False,  # Exclude text PKL
    include_image_pkl=True   # Include image PKL
)

# ============================================================================
# EXAMPLE 5: Create ID Mapping (See which IDs exist where)
# ============================================================================
print("\n" + "="*60)
print("EXAMPLE 5: ID Mapping")
print("="*60)

# Create a mapping of all IDs across ChromaDB and PKL files
id_mapping = engine.create_id_mapping()

print(f"Total unique IDs: {len(id_mapping)}")

# Check a specific ID
specific_id = "some_document_id"  # Replace with your ID
if specific_id in id_mapping:
    mapping_info = id_mapping[specific_id]
    print(f"\nID '{specific_id}' exists in:")
    print(f"  ChromaDB: {mapping_info.get('chroma', False)}")
    print(f"  Text PKL: {mapping_info.get('text_pkl', False)}")
    print(f"  Image PKL: {mapping_info.get('image_pkl', False)}")

# Count IDs in each source
chroma_count = sum(1 for v in id_mapping.values() if v.get('chroma'))
text_count = sum(1 for v in id_mapping.values() if v.get('text_pkl'))
image_count = sum(1 for v in id_mapping.values() if v.get('image_pkl'))

print(f"\nSummary:")
print(f"  IDs in ChromaDB: {chroma_count}")
print(f"  IDs in Text PKL: {text_count}")
print(f"  IDs in Image PKL: {image_count}")

# ============================================================================
# EXAMPLE 6: Get System Information
# ============================================================================
print("\n" + "="*60)
print("EXAMPLE 6: System Information")
print("="*60)

# Get information about your collections and data
info = engine.get_collection_info()

print("System Status:")
print(f"  ChromaDB Collection: {info['chroma']['name']}")
print(f"  ChromaDB Document Count: {info['chroma']['count']}")
print(f"  Text PKL Loaded: {info['text_pkl']['loaded']}")
print(f"  Text PKL Count: {info['text_pkl']['count']}")
print(f"  Image PKL Loaded: {info['image_pkl']['loaded']}")
print(f"  Image PKL Count: {info['image_pkl']['count']}")

# ============================================================================
# EXAMPLE 7: Search Using Pre-computed Embeddings
# ============================================================================
print("\n" + "="*60)
print("EXAMPLE 7: Search with Embeddings")
print("="*60)

# If you have pre-computed embeddings, use them directly
# query_embeddings = [[0.1, 0.2, 0.3, ...]]  # Your embedding vector(s)

# results = engine.search_by_embedding(
#     query_embeddings=query_embeddings,
#     top_k=5
# )

# ============================================================================
# EXAMPLE 8: Real-World Usage Pattern
# ============================================================================
print("\n" + "="*60)
print("EXAMPLE 8: Real-World Usage Pattern")
print("="*60)

def search_transcripts(query_text, num_results=10):
    """
    A helper function you can use in your application
    """
    # Initialize engine (you might want to do this once and reuse it)
    engine = SearchEngine()
    
    # Search
    results = engine.search(query=query_text, top_k=num_results)
    
    # Process results
    processed_results = []
    for result in results['results']:
        processed_results.append({
            'id': result['id'],
            'text': result['chroma']['document'],
            'similarity': 1 - result['chroma']['distance'],  # Convert distance to similarity
            'has_text_embedding': 'text_pkl' in result,
            'has_image_embedding': 'image_pkl' in result,
            'metadata': result['chroma'].get('metadata', {})
        })
    
    return processed_results

# Use the helper function
# search_results = search_transcripts("machine learning algorithms", num_results=5)
# for result in search_results:
#     print(f"ID: {result['id']}, Similarity: {result['similarity']:.3f}")
#     print(f"Text: {result['text'][:100]}...")

print("\n" + "="*60)
print("All examples shown! Use these patterns in your code.")
print("="*60)
