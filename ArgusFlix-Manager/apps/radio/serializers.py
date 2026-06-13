from rest_framework import serializers
from .models import RadioStation, RadioCategory

class RadioCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioCategory
        fields = '__all__'

class RadioStationSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = RadioStation
        fields = '__all__'
