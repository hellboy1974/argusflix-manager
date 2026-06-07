from django.db import models

class MediaServer(models.Model):
    SERVER_TYPES = [
        ('plex', 'Plex'),
        ('emby', 'Emby'),
        ('jellyfin', 'Jellyfin'),
    ]
    name = models.CharField(max_length=255)
    server_type = models.CharField(max_length=20, choices=SERVER_TYPES)
    base_url = models.URLField()
    api_token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    custom_properties = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name
