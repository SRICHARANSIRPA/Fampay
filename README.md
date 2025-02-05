# YouTube Video Fetcher

A Django-based service that automatically fetches and stores YouTube videos about cricket, with support for multiple API keys and Elasticsearch-powered search.

## Features

- Automatic YouTube video fetching every minute
- Multiple YouTube API key support with automatic fallback
- Elasticsearch integration for fast and efficient searching
- REST API endpoints for video retrieval
- Pagination support
- Celery-based background tasks
- Comprehensive logging system



## API Endpoints

- `GET /api/videos/` - List all videos (paginated)
- `GET /api/videos/?search=query` - Search videos by title/description
- `GET /api/videos/<id>/` - Get specific video details

## Architecture

- Django REST framework for API endpoints
- Celery for background tasks
- Elasticsearch for efficient searching
- Multiple API key support with automatic fallback
- Comprehensive logging system

## Project Structure

## Logging

Logs are stored in `logs/youtube_fetcher.log` with the following information:
- API key usage and rotation
- Video fetch operations
- Search operations
- Error tracking

# Django Project Setup Guide

## Prerequisites
Ensure you have the following installed:
- Python (3.x recommended)
- pip (Python package manager)
- Redis (for Celery workers)
- Elasticsearch (if required by the project)

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create a Django Project
```bash
django-admin startproject core .
```

### 3. Create a Django App
```bash
django-admin startapp videos
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```
Access the application at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 6. Start Celery Workers
```bash
celery -A core worker -l info
```

### 7. Start Celery Beat Scheduler
```bash
celery -A core beat -l info
```

### 8. Add API Keys
```bash
python manage.py add_api_key "your_api_key_1"
python manage.py add_api_key "your_api_key_2"
```

### 9. Setup Elasticsearch
```bash
python manage.py setup_elasticsearch
```

## Notes
- Ensure Redis is running before starting Celery.
- Elasticsearch should be properly configured before running `setup_elasticsearch`.
- API keys are required for authentication; replace placeholders with actual keys.

Happy Coding! 🚀
