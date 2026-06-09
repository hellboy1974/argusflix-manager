from django.db import models
import secrets
from django.utils.text import slugify

class CustomPlaylist(models.Model):
    """Represents a custom playlist / export profile containing a subset of categories."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    token = models.CharField(max_length=64, unique=True, db_index=True, blank=True)
    is_active = models.BooleanField(default=True)
    custom_properties = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(16)
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class CustomPlaylistLiveMapping(models.Model):
    """Maps custom playlists to live TV channel groups."""
    playlist = models.ForeignKey(CustomPlaylist, on_delete=models.CASCADE, related_name="live_mappings")
    channel_group = models.ForeignKey("argusflix_manager_channels.ChannelGroup", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("playlist", "channel_group")
        ordering = ["order"]

class CustomPlaylistVODMapping(models.Model):
    """Maps custom playlists to VOD (Movies / Series) categories."""
    playlist = models.ForeignKey(CustomPlaylist, on_delete=models.CASCADE, related_name="vod_mappings")
    vod_category = models.ForeignKey("vod.VODCategory", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("playlist", "vod_category")
        ordering = ["order"]
