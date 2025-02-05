from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from videos.views import VideoViewSet

router = DefaultRouter()
router.register(r'videos', VideoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] 