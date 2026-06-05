from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CustomPlaylistViewSet

app_name = 'output'

router = DefaultRouter()
router.register(r'playlists', CustomPlaylistViewSet, basename='customplaylist')

urlpatterns = router.urls
