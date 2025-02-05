from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Video

@registry.register_document
class VideoDocument(Document):
    title = fields.TextField()
    description = fields.TextField()
    channel_name = fields.TextField()
    published_at = fields.DateField()
    video_id = fields.TextField()
    thumbnail_url = fields.TextField()
    
    class Index:
        name = 'videos'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }
    
    class Django:
        model = Video
        fields = [
            'created_at',
        ] 