"""
FastAPI Backend for Transcript Search and Mapping System
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from search_engine import SearchEngine
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Transcript Search API",
    description="API for searching transcript embeddings and mapping to PKL data",
    version="1.0.0"
)

# Enable CORS (allow frontend to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global search engine instance (initialized once)
engine: Optional[SearchEngine] = None


def get_engine():
    """Get or initialize the search engine"""
    global engine
    if engine is None:
        engine = SearchEngine()
    return engine


# Request/Response Models
class SearchRequest(BaseModel):
    query: str
    top_k: int = 10
    collection_name: Optional[str] = None
    include_text_pkl: bool = True
    include_image_pkl: bool = True
    filter_dict: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[Dict[str, Any]]


class GetByIdsRequest(BaseModel):
    ids: List[str]
    include_text_pkl: bool = True
    include_image_pkl: bool = True
    collection_name: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Transcript Search API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "POST /search": "Search transcripts",
            "GET /search": "Search transcripts (query params)",
            "POST /get-by-ids": "Get documents by IDs",
            "GET /info": "Get system information",
            "GET /map-ids": "Create ID mapping",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        engine = get_engine()
        return {"status": "healthy", "engine_loaded": engine is not None}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.post("/search", response_model=SearchResponse)
async def search_post(request: SearchRequest):
    """
    Search transcripts using POST request
    
    Request body:
    - query: Search query text
    - top_k: Number of results (default: 10)
    - collection_name: Optional collection name
    - include_text_pkl: Include text PKL data (default: True)
    - include_image_pkl: Include image PKL data (default: True)
    - filter_dict: Optional metadata filters
    """
    try:
        engine = get_engine()
        results = engine.search(
            query=request.query,
            top_k=request.top_k,
            collection_name=request.collection_name,
            include_text_pkl=request.include_text_pkl,
            include_image_pkl=request.include_image_pkl,
            filter_dict=request.filter_dict
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search", response_model=SearchResponse)
async def search_get(
    query: str = Query(..., description="Search query text"),
    top_k: int = Query(10, description="Number of results"),
    collection_name: Optional[str] = Query(None, description="Collection name"),
    include_text_pkl: bool = Query(True, description="Include text PKL data"),
    include_image_pkl: bool = Query(True, description="Include image PKL data")
):
    """
    Search transcripts using GET request
    
    Query parameters:
    - query: Search query text (required)
    - top_k: Number of results (default: 10)
    - collection_name: Optional collection name
    - include_text_pkl: Include text PKL data (default: True)
    - include_image_pkl: Include image PKL data (default: True)
    """
    try:
        engine = get_engine()
        results = engine.search(
            query=query,
            top_k=top_k,
            collection_name=collection_name,
            include_text_pkl=include_text_pkl,
            include_image_pkl=include_image_pkl
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get-by-ids")
async def get_by_ids_post(request: GetByIdsRequest):
    """
    Get documents by their IDs
    
    Request body:
    - ids: List of document IDs
    - include_text_pkl: Include text PKL data (default: True)
    - include_image_pkl: Include image PKL data (default: True)
    - collection_name: Optional collection name
    """
    try:
        engine = get_engine()
        results = engine.get_by_ids(
            ids=request.ids,
            include_text_pkl=request.include_text_pkl,
            include_image_pkl=request.include_image_pkl,
            collection_name=request.collection_name
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get-by-ids")
async def get_by_ids_get(
    ids: str = Query(..., description="Comma-separated list of document IDs"),
    include_text_pkl: bool = Query(True, description="Include text PKL data"),
    include_image_pkl: bool = Query(True, description="Include image PKL data"),
    collection_name: Optional[str] = Query(None, description="Collection name")
):
    """
    Get documents by their IDs using GET request
    
    Query parameters:
    - ids: Comma-separated list of document IDs (required)
    - include_text_pkl: Include text PKL data (default: True)
    - include_image_pkl: Include image PKL data (default: True)
    - collection_name: Optional collection name
    """
    try:
        id_list = [id.strip() for id in ids.split(",")]
        engine = get_engine()
        results = engine.get_by_ids(
            ids=id_list,
            include_text_pkl=include_text_pkl,
            include_image_pkl=include_image_pkl,
            collection_name=collection_name
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/info")
async def get_info(collection_name: Optional[str] = None):
    """
    Get system information
    
    Query parameters:
    - collection_name: Optional collection name
    """
    try:
        engine = get_engine()
        info = engine.get_collection_info(collection_name)
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/map-ids")
async def map_ids():
    """
    Create comprehensive ID mapping across all data sources
    """
    try:
        engine = get_engine()
        mapping = engine.create_id_mapping()
        return {
            "total_ids": len(mapping),
            "mapping": mapping
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
