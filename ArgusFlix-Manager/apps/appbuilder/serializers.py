from rest_framework import serializers
from .models import AppProfile, AppPage, AppWidget

class AppWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppWidget
        fields = ['id', 'page', 'widget_type', 'order', 'settings']

class AppPageSerializer(serializers.ModelSerializer):
    widgets = AppWidgetSerializer(many=True, read_only=True)

    class Meta:
        model = AppPage
        fields = ['id', 'profile', 'page_type', 'title', 'widgets']

class AppProfileSerializer(serializers.ModelSerializer):
    pages = AppPageSerializer(many=True, read_only=True)

    class Meta:
        model = AppProfile
        fields = ['id', 'name', 'is_default', 'description', 'pages', 'created_at', 'updated_at']
