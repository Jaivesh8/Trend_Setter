# API Usage Guide

## Starting the Server

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the server
python3 start_api.py

# Or directly
python3 api.py
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### 1. Search (POST)

**Endpoint:** `POST /search`

**Request Body:**
```json
{
  "query": "your search query",
  "top_k": 10,
  "include_text_pkl": true,
  "include_image_pkl": true
}
```

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "photography",
    "top_k": 5
  }'
```

**Example using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "photography",
        "top_k": 5
    }
)
results = response.json()
print(results)
```

---

### 2. Search (GET)

**Endpoint:** `GET /search`

**Query Parameters:**
- `query` (required): Search query text
- `top_k` (optional, default: 10): Number of results
- `include_text_pkl` (optional, default: true)
- `include_image_pkl` (optional, default: true)

**Example:**
```bash
curl "http://localhost:8000/search?query=photography&top_k=5"
```

**Example using Python:**
```python
import requests

response = requests.get(
    "http://localhost:8000/search",
    params={
        "query": "photography",
        "top_k": 5
    }
)
results = response.json()
```

---

### 3. Get by IDs (POST)

**Endpoint:** `POST /get-by-ids`

**Request Body:**
```json
{
  "ids": ["id1", "id2", "id3"],
  "include_text_pkl": true,
  "include_image_pkl": true
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/get-by-ids" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": ["123", "456", "789"]
  }'
```

---

### 4. Get by IDs (GET)

**Endpoint:** `GET /get-by-ids`

**Query Parameters:**
- `ids` (required): Comma-separated list of IDs
- `include_text_pkl` (optional, default: true)
- `include_image_pkl` (optional, default: true)

**Example:**
```bash
curl "http://localhost:8000/get-by-ids?ids=123,456,789"
```

---

### 5. Get System Info

**Endpoint:** `GET /info`

**Example:**
```bash
curl "http://localhost:8000/info"
```

**Response:**
```json
{
  "chroma": {
    "name": "reel_text",
    "count": 1134
  },
  "text_pkl": {
    "count": 1134,
    "loaded": true
  },
  "image_pkl": {
    "count": 1123,
    "loaded": true
  }
}
```

---

### 6. Create ID Mapping

**Endpoint:** `GET /map-ids`

**Example:**
```bash
curl "http://localhost:8000/map-ids"
```

---

### 7. Health Check

**Endpoint:** `GET /health`

**Example:**
```bash
curl "http://localhost:8000/health"
```

---

## Response Format

### Search Response
```json
{
  "query": "photography",
  "total_results": 5,
  "results": [
    {
      "id": "document_id",
      "chroma": {
        "distance": 0.5,
        "document": "Full text...",
        "metadata": {...}
      },
      "text_pkl": {
        "embedding": [...],
        "metadata": {...}
      },
      "image_pkl": {
        "embedding": [...],
        "metadata": {...}
      }
    }
  ]
}
```

---

## Frontend Integration Examples

### React/JavaScript
```javascript
// Search function
async function searchTranscripts(query, topK = 10) {
  const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}&top_k=${topK}`);
  const data = await response.json();
  return data;
}

// Usage
const results = await searchTranscripts("photography", 5);
console.log(results.results);
```

### Python Client
```python
import requests

class TranscriptSearchClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def search(self, query, top_k=10):
        response = requests.get(
            f"{self.base_url}/search",
            params={"query": query, "top_k": top_k}
        )
        return response.json()
    
    def get_by_ids(self, ids):
        response = requests.get(
            f"{self.base_url}/get-by-ids",
            params={"ids": ",".join(ids)}
        )
        return response.json()

# Usage
client = TranscriptSearchClient()
results = client.search("photography", top_k=5)
```

---

## CORS Configuration

The API has CORS enabled for all origins by default. For production, update the CORS settings in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Error Handling

All endpoints return proper HTTP status codes:
- `200`: Success
- `500`: Server error (with error details in response)

Error response format:
```json
{
  "detail": "Error message here"
}
```
