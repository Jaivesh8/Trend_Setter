"""
Test the API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_search_get():
    """Test GET /search endpoint"""
    print("=" * 60)
    print("Testing GET /search")
    print("=" * 60)
    
    response = requests.get(
        f"{BASE_URL}/search",
        params={
            "query": "photography",
            "top_k": 3
        }
    )
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Query: {data['query']}")
    print(f"Total Results: {data['total_results']}")
    print(f"\nFirst Result:")
    if data['results']:
        result = data['results'][0]
        print(f"  ID: {result['id']}")
        print(f"  Text: {result['chroma']['document'][:100]}...")
        print(f"  Distance: {result['chroma']['distance']}")
    print()


def test_search_post():
    """Test POST /search endpoint"""
    print("=" * 60)
    print("Testing POST /search")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/search",
        json={
            "query": "college",
            "top_k": 2
        }
    )
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Query: {data['query']}")
    print(f"Total Results: {data['total_results']}")
    print()


def test_get_by_ids():
    """Test GET /get-by-ids endpoint"""
    print("=" * 60)
    print("Testing GET /get-by-ids")
    print("=" * 60)
    
    # First, get some IDs from a search
    search_response = requests.get(
        f"{BASE_URL}/search",
        params={"query": "test", "top_k": 2}
    )
    search_data = search_response.json()
    
    if search_data['results']:
        ids = [r['id'] for r in search_data['results']]
        ids_str = ",".join(ids)
        
        response = requests.get(
            f"{BASE_URL}/get-by-ids",
            params={"ids": ids_str}
        )
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Retrieved {len(data.get('chroma', {}).get('ids', []))} documents")
        print()


def test_info():
    """Test GET /info endpoint"""
    print("=" * 60)
    print("Testing GET /info")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/info")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2))
    print()


def test_health():
    """Test GET /health endpoint"""
    print("=" * 60)
    print("Testing GET /health")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2))
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("API Testing")
    print("=" * 60)
    print("Make sure the API server is running: python3 start_api.py")
    print()
    
    try:
        # Test health first
        test_health()
        
        # Test endpoints
        test_search_get()
        test_search_post()
        test_get_by_ids()
        test_info()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API server.")
        print("Please start the server first: python3 start_api.py")
    except Exception as e:
        print(f"Error: {e}")
