# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 20:41:32 2024

@author: adity
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# -------------------- Database Models -------------------- #

class Document(db.Model):
    """
    Model for storing documents in the database.
    Each document has a title, content, date added, and optionally an embedding.
    """
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    embedding = db.Column(db.LargeBinary, nullable=True)  # Optional, store embeddings

    def __repr__(self):
        return f'<Document {self.title}>'


class User(db.Model):
    """
    Model for storing user information for rate limiting and tracking API requests.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    request_count = db.Column(db.Integer, default=0)
    last_request_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.user_id}>'
