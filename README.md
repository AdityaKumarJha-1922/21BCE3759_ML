# 21BCE3759_ML

Aditya Kumar Jha


# Flask Document Retrieval System with News Scraping Service

## Overview

This project is a Flask-based backend system for document retrieval. It is designed to provide relevant context for LLMs (Large Language Models) using stored documents in a PostgreSQL database. It also includes a background news scraping service that periodically scrapes news articles and stores them in the database.

## Features

- **Document Retrieval API**: Allows users to search for relevant documents based on a query.
- **Background Scraping Service**: Periodically scrapes news articles from specified websites and stores them in the database.
- **Rate Limiting**: Limits users to 5 API requests and returns HTTP 429 for excessive requests.
- **Dockerized**: The entire system is containerized using Docker and Docker Compose for easy deployment.
- **Caching**: Provides faster document retrieval using a caching mechanism.
- **Logging and Monitoring**: Logs each request and tracks inference times for API calls.

## Requirements

- **Docker** and **Docker Compose** should be installed.
- **Python 3.11** and the following libraries are required:
  - Flask
  - Flask-SQLAlchemy
  - psycopg2-binary (for PostgreSQL connection)
  - requests (for scraping)
  - beautifulsoup4 (for HTML parsing)
  - schedule (for scheduling periodic tasks)
  - threading (for running background tasks)

## Installation

### 1. Clone the Repository



