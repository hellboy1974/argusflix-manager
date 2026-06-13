from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import RadioStationViewSet, RadioCategoryViewSet

router = DefaultRouter()
router.register(r'categories', RadioCategoryViewSet, basename='radiocategory')
router.register(r'stations', RadioStationViewSet, basename='radiostation')

urlpatterns = [
    path('', include(router.urls)),
]
