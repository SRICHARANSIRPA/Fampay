from django.core.management.base import BaseCommand
from videos.models import YouTubeAPIKey
import logging

logger = logging.getLogger('youtube_fetcher')

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('api_key', type=str, help='The YouTube API key to add')

    def handle(self, *args, **options):
        api_key = options['api_key']
        key, created = YouTubeAPIKey.objects.get_or_create(key=api_key)
        if created:
            logger.info(f"Successfully added new API key: {api_key[:8]}...")
        else:
            logger.info(f"API key already exists: {api_key[:8]}...") 