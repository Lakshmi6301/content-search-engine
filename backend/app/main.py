# main.py
# main.py
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from serpapi import GoogleSearch
from dotenv import load_dotenv


env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")


app = FastAPI(title="Content Search Engine")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    """Health check endpoint."""
    return {"message": "✅ Backend is running and SerpAPI connected!"}


# --- Helper function for SerpAPI ---
def serpapi_search(query: str, num: int = 10):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num
    }
    search = GoogleSearch(params)
    return search.get_dict()


# --- /search endpoint ---
@app.get("/search")
def search(query: str = Query(..., description="Search query"), limit: int = 10):
    """Return structured search results from SerpAPI."""
    if not SERPAPI_KEY:
        return {"error": "❌ SERPAPI_KEY not found in backend .env"}

    try:
        raw = serpapi_search(query, num=limit)
        results = []
        for r in raw.get("organic_results", [])[:limit]:
            results.append({
                "title": r.get("title") or "No Title",
                "snippet": r.get("snippet") or "No description available.",
                "link": r.get("link") or r.get("displayed_link") or "#"
            })
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}


# --- /suggest endpoint (autocomplete) ---
@app.get("/suggest")
def suggest(q: str = Query(..., min_length=1), limit: int = 5):
    """Quick suggestion API for autocomplete."""
    if not SERPAPI_KEY:
        return {"error": "❌ SERPAPI_KEY not found in backend .env"}

    try:
        raw = serpapi_search(q, num=limit)
        suggestions = []
        for r in raw.get("organic_results", [])[:limit]:
            title = r.get("title") or r.get("snippet") or r.get("link") or "No Title"
            suggestions.append({
                "title": title,
                "link": r.get("link", "#")
            })
        return {"suggestions": suggestions}
    except Exception as e:
        return {"error": str(e)}
