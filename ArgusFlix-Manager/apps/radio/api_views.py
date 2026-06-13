from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import RadioStation, RadioCategory
from .serializers import RadioStationSerializer, RadioCategorySerializer

class RadioCategoryViewSet(viewsets.ModelViewSet):
    queryset = RadioCategory.objects.all().order_by('sort_order', 'name')
    serializer_class = RadioCategorySerializer
    permission_classes = [IsAuthenticated]

class RadioStationViewSet(viewsets.ModelViewSet):
    queryset = RadioStation.objects.all().order_by('sort_order', 'name')
    serializer_class = RadioStationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = RadioStation.objects.all().order_by('sort_order', 'name')
        if 'is_active' in self.request.query_params:
            is_active = self.request.query_params.get('is_active').lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        return queryset
