# 🚀 Quick Start: Backend API

## Start the Server

```bash
python3 start_api.py
```

Server runs at: **http://localhost:8000**

## Test It Works

### Option 1: Browser
Visit: http://localhost:8000/docs

### Option 2: Command Line
```bash
# Health check
curl http://localhost:8000/health

# Search
curl "http://localhost:8000/search?query=photography&top_k=3"
```

### Option 3: Python Test
```bash
python3 test_api.py
```

## Available Endpoints

| Endpoint | Method | What It Does |
|----------|--------|--------------|
| `/search` | GET/POST | Search transcripts |
| `/get-by-ids` | GET/POST | Get documents by IDs |
| `/info` | GET | System information |
| `/map-ids` | GET | Create ID mapping |
| `/health` | GET | Health check |
| `/docs` | GET | API documentation |

## Example: Search from Frontend

### JavaScript
```javascript
fetch('http://localhost:8000/search?query=photography&top_k=5')
  .then(res => res.json())
  .then(data => {
    console.log(data.results);
  });
```

### Python
```python
import requests
response = requests.get('http://localhost:8000/search', params={
    'query': 'photography',
    'top_k': 5
})
results = response.json()
```

## That's It!

Your backend is ready to connect to any frontend! 🎉
