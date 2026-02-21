# Transcript Search & Mapping API

FastAPI backend for searching transcript embeddings stored in ChromaDB and mapping them with vectorized data from PKL files. Designed for integration with Kotlin frontend applications.

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run Server

```bash
python3 start_api.py
```

Server runs at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/search` | GET/POST | Search transcripts |
| `/get-by-ids` | GET/POST | Get documents by IDs |
| `/info` | GET | System information |
| `/health` | GET | Health check |

## 📱 Kotlin Integration

### Retrofit Setup

```kotlin
interface TranscriptApi {
    @GET("search")
    fun search(
        @Query("query") query: String,
        @Query("top_k") topK: Int = 10
    ): Call<SearchResponse>
}
```

See `README_GITHUB.md` for complete Kotlin integration examples.

## 📁 Project Structure

```
.
├── api.py              # FastAPI backend server
├── start_api.py        # Server startup script
├── search_engine.py     # Main search engine
├── chroma_manager.py   # ChromaDB operations
├── pkl_loader.py       # PKL file loader
├── mapper.py           # Data mapping utilities
├── config.py           # Configuration
└── requirements.txt    # Dependencies
```

## 🔧 Configuration

Update `config.py` to customize:
- Database paths
- Default search parameters
- Collection names

## 📚 Documentation

- `API_USAGE.md` - Complete API documentation
- `BACKEND_SETUP.md` - Setup and deployment guide
- `README_GITHUB.md` - GitHub and Kotlin integration guide

## 🛠️ Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python3 start_api.py

# Test API
python3 test_api.py
```

## 📝 License

[Your License Here]
