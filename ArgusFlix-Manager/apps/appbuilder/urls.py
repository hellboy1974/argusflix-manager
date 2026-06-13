from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppProfileViewSet, AppPageViewSet, AppWidgetViewSet

router = DefaultRouter()
router.register(r'profiles', AppProfileViewSet)
router.register(r'pages', AppPageViewSet)
router.register(r'widgets', AppWidgetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
