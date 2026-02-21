"""
Main interface for transcript search and mapping system
"""
import argparse
import json
from search_engine import SearchEngine
import config


def print_results(results: dict, format_json: bool = False):
    """Pretty print search results"""
    if format_json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print("\n" + "="*80)
        print(f"Query: {results.get('query', 'N/A')}")
        print(f"Total Results: {results.get('total_results', 0)}")
        print("="*80)
        
        if 'results' in results:
            # Unified format
            for i, result in enumerate(results['results'], 1):
                print(f"\n--- Result {i} ---")
                print(f"ID: {result.get('id')}")
                
                chroma = result.get('chroma', {})
                if chroma:
                    print(f"Distance: {chroma.get('distance')}")
                    print(f"Document: {chroma.get('document', '')[:200]}...")
                    if chroma.get('metadata'):
                        print(f"Metadata: {chroma.get('metadata')}")
                
                if 'text_pkl' in result:
                    print("✓ Text PKL data available")
                
                if 'image_pkl' in result:
                    print("✓ Image PKL data available")
        else:
            # Separate format
            if 'chroma' in results:
                print("\nChromaDB Results:")
                chroma = results['chroma']
                ids = chroma.get('ids', [[]])[0] if chroma.get('ids') else []
                print(f"Found {len(ids)} results")
            
            if 'text_pkl' in results:
                print(f"\nText PKL: {len(results['text_pkl'].get('ids', []))} items")
            
            if 'image_pkl' in results:
                print(f"\nImage PKL: {len(results['image_pkl'].get('ids', []))} items")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Transcript Search and Mapping System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  python main.py search "your query here"
  
  # Search with specific number of results
  python main.py search "your query" --top-k 20
  
  # Get info about collections
  python main.py info
  
  # Get specific documents by IDs
  python main.py get-by-ids id1 id2 id3
  
  # Create ID mapping
  python main.py map-ids
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search transcripts')
    search_parser.add_argument('query', help='Search query text')
    search_parser.add_argument('--top-k', type=int, default=config.DEFAULT_TOP_K,
                              help=f'Number of results (default: {config.DEFAULT_TOP_K})')
    search_parser.add_argument('--collection', type=str, default=None,
                              help='Specific collection name')
    search_parser.add_argument('--no-text', action='store_true',
                              help='Exclude text PKL data')
    search_parser.add_argument('--no-image', action='store_true',
                              help='Exclude image PKL data')
    search_parser.add_argument('--json', action='store_true',
                              help='Output as JSON')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get system information')
    info_parser.add_argument('--collection', type=str, default=None,
                            help='Specific collection name')
    info_parser.add_argument('--json', action='store_true',
                            help='Output as JSON')
    
    # Get by IDs command
    get_parser = subparsers.add_parser('get-by-ids', help='Get documents by IDs')
    get_parser.add_argument('ids', nargs='+', help='Document IDs')
    get_parser.add_argument('--no-text', action='store_true',
                          help='Exclude text PKL data')
    get_parser.add_argument('--no-image', action='store_true',
                          help='Exclude image PKL data')
    get_parser.add_argument('--json', action='store_true',
                          help='Output as JSON')
    
    # Map IDs command
    map_parser = subparsers.add_parser('map-ids', help='Create ID mapping')
    map_parser.add_argument('--json', action='store_true',
                          help='Output as JSON')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize search engine
    try:
        engine = SearchEngine()
    except Exception as e:
        print(f"Error initializing search engine: {e}")
        return
    
    # Execute command
    try:
        if args.command == 'search':
            results = engine.search(
                query=args.query,
                top_k=args.top_k,
                collection_name=args.collection,
                include_text_pkl=not args.no_text,
                include_image_pkl=not args.no_image
            )
            print_results(results, format_json=args.json)
        
        elif args.command == 'info':
            info = engine.get_collection_info(args.collection)
            if args.json:
                print(json.dumps(info, indent=2, default=str))
            else:
                print("\n" + "="*80)
                print("System Information")
                print("="*80)
                print(f"\nChromaDB Collection: {info['chroma']['name']}")
                print(f"ChromaDB Count: {info['chroma']['count']}")
                print(f"\nText PKL: {'Loaded' if info['text_pkl']['loaded'] else 'Not loaded'}")
                print(f"Text PKL Count: {info['text_pkl']['count']}")
                print(f"\nImage PKL: {'Loaded' if info['image_pkl']['loaded'] else 'Not loaded'}")
                print(f"Image PKL Count: {info['image_pkl']['count']}")
                if info['available_collections']:
                    print(f"\nAvailable Collections: {', '.join(info['available_collections'])}")
        
        elif args.command == 'get-by-ids':
            results = engine.get_by_ids(
                ids=args.ids,
                include_text_pkl=not args.no_text,
                include_image_pkl=not args.no_image,
                collection_name=getattr(args, 'collection', None)
            )
            if args.json:
                print(json.dumps(results, indent=2, default=str))
            else:
                print("\n" + "="*80)
                print(f"Retrieved {len(args.ids)} document(s)")
                print("="*80)
                print(json.dumps(results, indent=2, default=str))
        
        elif args.command == 'map-ids':
            mapping = engine.create_id_mapping()
            if args.json:
                print(json.dumps(mapping, indent=2, default=str))
            else:
                print("\n" + "="*80)
                print("ID Mapping")
                print("="*80)
                print(f"Total IDs: {len(mapping)}")
                chroma_count = sum(1 for v in mapping.values() if v.get('chroma'))
                text_count = sum(1 for v in mapping.values() if v.get('text_pkl'))
                image_count = sum(1 for v in mapping.values() if v.get('image_pkl'))
                print(f"In ChromaDB: {chroma_count}")
                print(f"In Text PKL: {text_count}")
                print(f"In Image PKL: {image_count}")
    
    except Exception as e:
        print(f"Error executing command: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
