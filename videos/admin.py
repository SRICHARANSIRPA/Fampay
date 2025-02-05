from django.contrib import admin
from .models import Video, YouTubeAPIKey
import logging

logger = logging.getLogger('youtube_fetcher')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel_name', 'published_at', 'created_at')
    search_fields = ('title', 'description', 'channel_name')
    list_filter = ('channel_name', 'published_at')

@admin.register(YouTubeAPIKey)
class YouTubeAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('key_preview', 'is_active', 'quota_exceeded', 'last_used')
    list_filter = ('is_active', 'quota_exceeded')
    actions = ['reset_quota_exceeded']
    
    def key_preview(self, obj):
        return f"{obj.key[:8]}..."
    key_preview.short_description = 'API Key'
    
    def reset_quota_exceeded(self, request, queryset):
        count = queryset.filter(quota_exceeded=True).update(quota_exceeded=False)
        logger.info(f"Reset quota exceeded flag for {count} API keys")
        self.message_user(request, f"Reset quota exceeded flag for {count} API keys")
    reset_quota_exceeded.short_description = "Reset quota exceeded status" 