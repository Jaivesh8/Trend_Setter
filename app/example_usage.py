"""
Example usage of the transcript search and mapping system
"""
from search_engine import SearchEngine
import json


def example_basic_search():
    """Example: Basic text search"""
    print("="*80)
    print("Example 1: Basic Text Search")
    print("="*80)
    
    engine = SearchEngine()
    
    # Perform a search
    results = engine.search(
        query="your search query here",
        top_k=5
    )
    
    print(f"\nFound {results['total_results']} results")
    for i, result in enumerate(results['results'], 1):
        print(f"\nResult {i}:")
        print(f"  ID: {result['id']}")
        print(f"  Distance: {result['chroma']['distance']}")
        print(f"  Document: {result['chroma']['document'][:100]}...")


def example_search_with_filters():
    """Example: Search with metadata filters"""
    print("\n" + "="*80)
    print("Example 2: Search with Filters")
    print("="*80)
    
    engine = SearchEngine()
    
    # Search with metadata filter
    results = engine.search(
        query="your query",
        top_k=10,
        filter_dict={"category": "transcript"}  # Example filter
    )
    
    print(f"Found {results['total_results']} filtered results")


def example_get_by_ids():
    """Example: Retrieve specific documents by IDs"""
    print("\n" + "="*80)
    print("Example 3: Get Documents by IDs")
    print("="*80)
    
    engine = SearchEngine()
    
    # First, get some IDs from a search
    search_results = engine.search(query="example", top_k=3)
    ids = [r['id'] for r in search_results['results']]
    
    # Then retrieve full data for those IDs
    full_data = engine.get_by_ids(ids)
    
    print(f"Retrieved data for {len(ids)} documents")
    print(f"ChromaDB data: {len(full_data['chroma'].get('ids', []))} items")
    print(f"Text PKL data: {len(full_data['text_pkl'].get('ids', []))} items")
    print(f"Image PKL data: {len(full_data['image_pkl'].get('ids', []))} items")


def example_id_mapping():
    """Example: Create ID mapping across all data sources"""
    print("\n" + "="*80)
    print("Example 4: ID Mapping")
    print("="*80)
    
    engine = SearchEngine()
    
    # Create comprehensive mapping
    mapping = engine.create_id_mapping()
    
    print(f"Total unique IDs: {len(mapping)}")
    
    # Count IDs in each source
    chroma_only = sum(1 for v in mapping.values() if v.get('chroma') and not v.get('text_pkl') and not v.get('image_pkl'))
    text_only = sum(1 for v in mapping.values() if v.get('text_pkl') and not v.get('chroma') and not v.get('image_pkl'))
    image_only = sum(1 for v in mapping.values() if v.get('image_pkl') and not v.get('chroma') and not v.get('text_pkl'))
    all_sources = sum(1 for v in mapping.values() if v.get('chroma') and v.get('text_pkl') and v.get('image_pkl'))
    
    print(f"IDs in ChromaDB only: {chroma_only}")
    print(f"IDs in Text PKL only: {text_only}")
    print(f"IDs in Image PKL only: {image_only}")
    print(f"IDs in all sources: {all_sources}")


def example_collection_info():
    """Example: Get system information"""
    print("\n" + "="*80)
    print("Example 5: Collection Information")
    print("="*80)
    
    engine = SearchEngine()
    
    info = engine.get_collection_info()
    
    print("System Information:")
    print(json.dumps(info, indent=2, default=str))


def example_search_text_only():
    """Example: Search with only text PKL data"""
    print("\n" + "="*80)
    print("Example 6: Search Text PKL Only")
    print("="*80)
    
    engine = SearchEngine()
    
    results = engine.search(
        query="your query",
        top_k=5,
        include_text_pkl=True,
        include_image_pkl=False  # Exclude image data
    )
    
    print(f"Found {results['total_results']} results")
    for result in results['results']:
        if 'text_pkl' in result:
            print(f"ID {result['id']} has text PKL data")


def example_unified_vs_separate():
    """Example: Compare unified vs separate result formats"""
    print("\n" + "="*80)
    print("Example 7: Unified vs Separate Formats")
    print("="*80)
    
    engine = SearchEngine()
    
    # Unified format (default)
    unified = engine.search(
        query="example",
        top_k=3,
        unified_format=True
    )
    print("Unified format:")
    print(f"  Type: {type(unified)}")
    print(f"  Keys: {list(unified.keys())}")
    
    # Separate format
    separate = engine.search(
        query="example",
        top_k=3,
        unified_format=False
    )
    print("\nSeparate format:")
    print(f"  Type: {type(separate)}")
    print(f"  Keys: {list(separate.keys())}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Transcript Search and Mapping System - Examples")
    print("="*80)
    
    # Run examples
    try:
        example_basic_search()
        example_get_by_ids()
        example_id_mapping()
        example_collection_info()
        example_search_text_only()
        example_unified_vs_separate()
        
        print("\n" + "="*80)
        print("All examples completed!")
        print("="*80)
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()
