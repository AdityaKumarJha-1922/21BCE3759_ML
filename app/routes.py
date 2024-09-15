# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 20:42:50 2024

@author: adity
"""

from flask import Blueprint, request, jsonify
from utils import retrieve_documents, rate_limit_user, log_inference_time
import time

# Define a blueprint for the routes
routes = Blueprint('routes', __name__)

# -------------------- API Routes -------------------- #

@routes.route('/health', methods=['GET'])
def health():
    """
    Health check route to confirm the API is running.
    """
    return jsonify({"status": "API is running"}), 200


@routes.route('/search', methods=['GET'])
def search():
    """
    Search route that retrieves the top matching documents based on the query.
    
    Query parameters:
    - text: The input text to search for.
    - top_k: The number of top results to return (default: 5).
    - threshold: Similarity threshold for filtering results (default: 0.8).
    - user_id: Unique identifier for the user making the request.
    
    Rate limits users to 5 requests per 24 hours.
    """
    start_time = time.time()
    
    # Get query parameters from the request
    query_text = request.args.get('text', '')
    top_k = int(request.args.get('top_k', 5))
    threshold = float(request.args.get('threshold', 0.8))
    user_id = request.args.get('user_id', '')
    
    # Rate limit check
    if not rate_limit_user(user_id):
        return jsonify({"error": "Too many requests"}), 429
    
    # Perform document retrieval
    results = retrieve_documents(query_text, top_k, threshold)
    
    # Log inference time
    inference_time = log_inference_time(start_time)
    
    return jsonify({"results": results, "inference_time": inference_time}), 200

