# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 21:06:53 2024

@author: adity
"""

from flask import Flask, request, jsonify
from utils import retrieve_documents, rate_limit_user, log_inference_time
import time
from routes import routes
from models import db
from flask_migrate import Migrate

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is running"}), 200


@app.route('/search', methods=['GET'])
def search():
    start_time = time.time()
    
    query_text = request.args.get('text', '')
    top_k = int(request.args.get('top_k', 5))
    threshold = float(request.args.get('threshold', 0.8))
    user_id = request.args.get('user_id', '')
    
    # Check rate limit
    if not rate_limit_user(user_id):
        return jsonify({"error": "Too many requests"}), 429
    
    # Perform document retrieval
    results = retrieve_documents(query_text, top_k, threshold)
    
    # Log inference time
    inference_time = log_inference_time(start_time)
    
    return jsonify({"results": results, "inference_time": inference_time}), 200


app.register_blueprint(routes)

# Configure PostgreSQL Database URI (replace with your own credentials)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Set up migration support
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
