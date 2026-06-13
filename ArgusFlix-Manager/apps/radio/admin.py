from django.contrib import admin
from .models import RadioStation

@admin.register(RadioStation)
class RadioStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'sort_order', 'is_active', 'updated_at')
    list_filter = ('is_active', 'genre')
    search_fields = ('name', 'genre', 'stream_url')
    ordering = ('sort_order', 'name')
