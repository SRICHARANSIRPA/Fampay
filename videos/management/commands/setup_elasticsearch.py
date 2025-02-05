from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry
import logging

logger = logging.getLogger('youtube_fetcher')

class Command(BaseCommand):
    help = 'Creates the Elasticsearch index and indexes all documents'

    def handle(self, *args, **options):
        try:
            # Create indices
            for index in registry.get_indices():
                logger.info(f"Creating index: {index._name}")
                index.create()
                
            # Index all documents
            for doc in registry.get_documents():
                logger.info(f"Indexing {doc._doc_type.model.__name__} documents")
                doc().update(doc._doc_type.model.objects.all())
                
            logger.info("Successfully set up Elasticsearch indices")
            
        except Exception as e:
            logger.error(f"Error setting up Elasticsearch: {str(e)}") 