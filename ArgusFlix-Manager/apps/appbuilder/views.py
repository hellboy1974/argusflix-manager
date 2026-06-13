from rest_framework import viewsets
from .models import AppProfile, AppPage, AppWidget
from .serializers import AppProfileSerializer, AppPageSerializer, AppWidgetSerializer

class AppProfileViewSet(viewsets.ModelViewSet):
    queryset = AppProfile.objects.all()
    serializer_class = AppProfileSerializer

class AppPageViewSet(viewsets.ModelViewSet):
    queryset = AppPage.objects.all()
    serializer_class = AppPageSerializer
    filterset_fields = ['profile', 'page_type']

class AppWidgetViewSet(viewsets.ModelViewSet):
    queryset = AppWidget.objects.all()
    serializer_class = AppWidgetSerializer
    filterset_fields = ['page', 'widget_type']
