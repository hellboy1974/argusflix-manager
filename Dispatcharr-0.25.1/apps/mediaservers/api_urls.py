from rest_framework.routers import DefaultRouter
from .api_views import MediaServerViewSet

router = DefaultRouter()
router.register(r'', MediaServerViewSet, basename='mediaserver')

urlpatterns = router.urls
