from rest_framework import serializers
from .models import MediaServer

class MediaServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaServer
        fields = '__all__'
        extra_kwargs = {
            'api_token': {'write_only': True}
        }
