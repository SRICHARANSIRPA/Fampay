from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from elasticsearch_dsl import Q
from .models import Video
from .serializers import VideoSerializer
from .documents import VideoDocument

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        
        if search_query:
            # Elasticsearch for searching videos
            q = Q('multi_match', query=search_query, fields=['title', 'description'])
            search = VideoDocument.search().query(q)
            
            # Paginate results
            page = self.paginate_queryset(search[:100].to_queryset())
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
                
            serializer = self.get_serializer(search.to_queryset(), many=True)
            return Response(serializer.data)
            
        return super().list(request, *args, **kwargs) 