from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import time

app = FastAPI()

# Redis client for caching
cache = redis.StrictRedis(host='localhost', port=6379, db=0)


# Sample health check endpoint
@app.get("/health")
def health():
    return {"status": "API is running"}


# Model for search request
class SearchRequest(BaseModel):
    text: str
    top_k: int = 5
    threshold: float = 0.5
    user_id: int


# Sample search endpoint
@app.post("/search")
def search(req: SearchRequest):
    # Dummy search logic; Replace with real retrieval logic
    start_time = time.time()

    # Check if user exceeded rate limit
    user_key = f"user:{req.user_id}:requests"
    user_requests = cache.get(user_key)

    if user_requests and int(user_requests) >= 5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Simulate document search (Replace with actual document retrieval and similarity check)
    search_results = [{"doc": "Sample Document 1", "score": 0.9}]

    # Increment request count for the user
    cache.incr(user_key)
    cache.expire(user_key, 60 * 60)  # Reset every hour

    # Log inference time
    inference_time = time.time() - start_time

    return {
        "results": search_results,
        "inference_time": inference_time
    }

import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="document_db",
    user="myuser",
    password="mypassword"

)

def store_document(content: str):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (content) VALUES (%s) RETURNING id;", (content,))
    doc_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return doc_id

# Dummy document retrieval (You will later use embeddings to retrieve relevant documents)
def get_similar_documents(query: str, top_k: int, threshold: float):
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM documents;")
    documents = cursor.fetchall()
    cursor.close()

    # Here, we would calculate similarity with embeddings
    return [{"doc": doc[0], "score": 0.9} for doc in documents][:top_k]

def cache_search_results(user_id: int, results: list):
    cache.set(f"search:{user_id}", str(results), ex=3600)

def get_cached_results(user_id: int):
    cached_results = cache.get(f"search:{user_id}")
    if cached_results:
        return eval(cached_results)  # Convert string back to list
    return None

@app.post("/search")
def search(req: SearchRequest):
    start_time = time.time()

    # Check if results are cached
    cached_results = get_cached_results(req.user_id)
    if cached_results:
        return {"results": cached_results, "cached": True}

    # Proceed with the search if not cached
    search_results = get_similar_documents(req.text, req.top_k, req.threshold)
    cache_search_results(req.user_id, search_results)

    inference_time = time.time() - start_time

    return {
        "results": search_results,
        "inference_time": inference_time,
        "cached": False
    }


