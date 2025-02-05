from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()
    channel_name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['description']),
            models.Index(fields=['published_at']),
        ]

    def __str__(self):
        return self.title 

class YouTubeAPIKey(models.Model):
    key = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    quota_exceeded = models.BooleanField(default=False)
    last_used = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key[:8]}... ({'Active' if self.is_active else 'Inactive'})"

    class Meta:
        ordering = ['last_used'] 