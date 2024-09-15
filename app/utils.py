# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 20:42:06 2024

@author: adity
"""

import redis
import time
import json
from sentence_transformers import SentenceTransformer, util

# Initialize the Redis client for caching
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Load the document encoder model (e.g., SentenceTransformer)
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


# -------------------- Document Retrieval Functions -------------------- #

def retrieve_documents(text: str, top_k: int, threshold: float):
    """
    Retrieve and rank documents based on the similarity of the input text.
    Caches the result in Redis for faster future lookups.
    
    Args:
        text (str): Input query text.
        top_k (int): Number of top results to return.
        threshold (float): Similarity threshold for filtering results.
    
    Returns:
        list: List of relevant documents.
    """
    # Check the cache first
    cached_result = r.get(text)
    if cached_result:
        return json.loads(cached_result)

    # If not cached, proceed with retrieval and encoding
    query_embedding = model.encode(text)
    documents = get_all_documents_from_db()  # Fetch documents from DB or file storage
    doc_embeddings = [model.encode(doc['content']) for doc in documents]
    
    # Perform semantic search to find top_k most relevant documents
    hits = util.semantic_search(query_embedding, doc_embeddings, top_k=top_k)
    
    # Filter results based on similarity threshold
    results = [documents[i] for i in hits[0] if hits[0][i]['score'] >= threshold]
    
    # Cache the result for faster future retrieval
    r.set(text, json.dumps(results), ex=3600)  # Cache for 1 hour
    
    return results


def get_all_documents_from_db():
    """
    Simulate fetching documents from the database. 
    In real application, this will involve querying a real database like PostgreSQL.
    
    Returns:
        list: List of documents with 'id' and 'content'.
    """
    # For simplicity, returning hardcoded documents. Replace this with DB queries.
    return [
        {"id": 1, "content": "Document 1 content"},
        {"id": 2, "content": "Document 2 content"},
        {"id": 3, "content": "Document 3 content"}
    ]


# -------------------- Caching and Rate Limiting Functions -------------------- #

def cache_result(key: str, value: dict, expiry: int = 3600):
    """
    Cache a key-value pair in Redis for a specified expiration time.
    
    Args:
        key (str): Cache key.
        value (dict): Cache value (usually the search result).
        expiry (int): Expiration time in seconds (default 1 hour).
    """
    r.set(key, json.dumps(value), ex=expiry)


def get_cached_result(key: str):
    """
    Retrieve a cached result from Redis by key.
    
    Args:
        key (str): Cache key.
    
    Returns:
        dict or None: Cached result if exists, otherwise None.
    """
    cached_result = r.get(key)
    if cached_result:
        return json.loads(cached_result)
    return None


def rate_limit_user(user_id: str):
    """
    Implement rate limiting by tracking the number of requests made by a user.
    If the user exceeds the allowed number of requests (5), return a rate limit error.
    
    Args:
        user_id (str): Unique ID of the user.
    
    Returns:
        bool: True if user is within the limit, False if rate limit is exceeded.
    """
    user_requests = r.get(user_id)
    
    if user_requests:
        user_requests = int(user_requests)
        
        if user_requests >= 5:
            return False  # Rate limit exceeded
        
        # Increment the request count
        r.incr(user_id)
    else:
        # New user, set the request count to 1
        r.set(user_id, 1, ex=86400)  # Limit is per 24 hours (86400 seconds)
    
    return True


# -------------------- Miscellaneous Utility Functions -------------------- #

def log_inference_time(start_time: float):
    """
    Calculate and log the inference time for a request.
    
    Args:
        start_time (float): Timestamp when the request started.
    
    Returns:
        float: Time taken for inference.
    """
    return time.time() - start_time
