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

## Prerequisites

- Python 3.x
- Redis Server
- Elasticsearch 8.x
- YouTube Data API v3 keys


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


pip install -r requirements.txt
django-admin startproject core .
django-admin startapp videos 
python manage.py makemigrations
python manage.py migrate 
python manage.py runserver 
celery -A core worker -l info
celery -A core beat -l info 
python manage.py add_api_key "your_api_key_1"
python manage.py add_api_key "your_api_key_2" 
python manage.py setup_elasticsearch 