from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppProfileViewSet, AppPageViewSet, AppWidgetViewSet
from .api_views import LayoutExportViewSet

router = DefaultRouter()
router.register(r'profiles', AppProfileViewSet)
router.register(r'pages', AppPageViewSet)
router.register(r'widgets', AppWidgetViewSet)
router.register(r'export', LayoutExportViewSet, basename='export')

urlpatterns = [
    path('', include(router.urls)),
]
