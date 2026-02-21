# Backend API Setup Guide

## ✅ What's Been Created

1. **`api.py`** - FastAPI backend server with all endpoints
2. **`start_api.py`** - Easy server startup script
3. **`test_api.py`** - Test script for API endpoints
4. **`API_USAGE.md`** - Complete API documentation

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- All other dependencies

### Step 2: Start the Server

```bash
python3 start_api.py
```

The server will start at: **http://localhost:8000**

### Step 3: Test the API

**Option A: Use the test script**
```bash
# In another terminal
python3 test_api.py
```

**Option B: Use curl**
```bash
# Health check
curl http://localhost:8000/health

# Search
curl "http://localhost:8000/search?query=photography&top_k=3"
```

**Option C: Visit in browser**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📡 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET/POST | `/search` | Search transcripts |
| GET/POST | `/get-by-ids` | Get documents by IDs |
| GET | `/info` | System information |
| GET | `/map-ids` | Create ID mapping |

## 🔌 Frontend Integration

### JavaScript/React Example

```javascript
// Search function
async function searchTranscripts(query) {
  const response = await fetch(
    `http://localhost:8000/search?query=${encodeURIComponent(query)}&top_k=10`
  );
  return await response.json();
}

// Usage
const results = await searchTranscripts("photography");
console.log(results.results);
```

### Python Client Example

```python
import requests

def search(query, top_k=10):
    response = requests.get(
        "http://localhost:8000/search",
        params={"query": query, "top_k": top_k}
    )
    return response.json()

# Usage
results = search("photography", top_k=5)
for result in results['results']:
    print(result['chroma']['document'])
```

## 🌐 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

You can set these in your environment:
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

## 🔒 Security Notes

1. **CORS**: Currently allows all origins. Update in `api.py` for production:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

2. **Rate Limiting**: Consider adding rate limiting for production

3. **Authentication**: Add authentication if needed:
   ```python
   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   @app.get("/search")
   async def search(credentials = Depends(security)):
       # Verify token
       pass
   ```

## 📝 Example Requests

### POST /search
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "photography",
    "top_k": 5,
    "include_text_pkl": true,
    "include_image_pkl": true
  }'
```

### GET /search
```bash
curl "http://localhost:8000/search?query=photography&top_k=5"
```

### POST /get-by-ids
```bash
curl -X POST "http://localhost:8000/get-by-ids" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": ["123", "456", "789"]
  }'
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Change port in start_api.py or api.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**CORS errors:**
- Check CORS settings in `api.py`
- Make sure frontend URL is in `allow_origins`

## 📚 Next Steps

1. Start the server: `python3 start_api.py`
2. Test endpoints: `python3 test_api.py`
3. Visit docs: http://localhost:8000/docs
4. Integrate with your frontend!
