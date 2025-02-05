import os
from datetime import datetime, timezone
import requests
from celery import shared_task
import logging
from django.conf import settings
from .models import Video, YouTubeAPIKey
from .documents import VideoDocument

logger = logging.getLogger('youtube_fetcher')
SEARCH_QUERY = 'cricket'

class QuotaExceededException(Exception):
    pass

def get_next_available_api_key():
    """Get the next available API key that hasn't exceeded its quota"""
    api_key = YouTubeAPIKey.objects.filter(
        is_active=True,
        quota_exceeded=False
    ).order_by('last_used').first()
    
    if not api_key:

        YouTubeAPIKey.objects.filter(quota_exceeded=True).update(quota_exceeded=False)
        api_key = YouTubeAPIKey.objects.filter(is_active=True).order_by('last_used').first()
        
    if not api_key:
        logger.error("No API keys available")
        raise Exception("No API keys available")
        
    return api_key

def handle_quota_exceeded(api_key):
    """Mark the current API key as quota exceeded"""
    logger.warning(f"API key {api_key.key[:8]}... has exceeded its quota")
    api_key.quota_exceeded = True
    api_key.save()

@shared_task
def fetch_youtube_videos():
    max_retries = YouTubeAPIKey.objects.filter(is_active=True).count()
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            api_key = get_next_available_api_key()
            
            url = 'https://www.googleapis.com/youtube/v3/search'
            params = {
                'part': 'snippet',
                'q': SEARCH_QUERY,
                'type': 'video',
                'maxResults': 50,
                'key': api_key.key,
                'order': 'date'
            }
            
            response = requests.get(url, params=params)
            
            # Check for quota exceeded error
            if response.status_code == 403:
                error_reason = response.json().get('error', {}).get('errors', [{}])[0].get('reason', '')
                if error_reason == 'quotaExceeded':
                    handle_quota_exceeded(api_key)
                    retry_count += 1
                    continue
                    
            response.raise_for_status()
            videos_data = response.json()
            
            videos_added = 0
            for item in videos_data.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                # Create or update video in database
                video, created = Video.objects.update_or_create(
                    video_id=video_id,
                    defaults={
                        'title': snippet['title'],
                        'description': snippet['description'],
                        'published_at': datetime.strptime(
                            snippet['publishedAt'], 
                            '%Y-%m-%dT%H:%M:%SZ'
                        ).replace(tzinfo=timezone.utc),
                        'thumbnail_url': snippet['thumbnails']['high']['url'],
                        'channel_name': snippet['channelTitle']
                    }
                )
                
                # Index in Elasticsearch
                VideoDocument().update(video)
                videos_added += 1
            
            logger.info(f"Successfully fetched and stored {videos_added} videos")
            return
            
        except Exception as e:
            logger.error(f"Error fetching videos: {str(e)}")
            retry_count += 1
    
    logger.error("All API keys exhausted or encountered errors") 