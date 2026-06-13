from django.db import models

class RadioCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Name of the radio category/genre")
    sort_order = models.IntegerField(default=0, help_text="Sort order for UI presentation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Radio Category"
        verbose_name_plural = "Radio Categories"

    def __str__(self):
        return self.name

class RadioStation(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the radio station")
    stream_url = models.URLField(max_length=1024, help_text="Stream URL (MP3, AAC, HLS)")
    logo_url = models.URLField(max_length=1024, blank=True, null=True, help_text="URL to the station's logo")
    category = models.ForeignKey(RadioCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='stations', help_text="Radio Category/Genre")
    sort_order = models.IntegerField(default=0, help_text="Sort order for UI presentation")
    is_active = models.BooleanField(default=True, help_text="Whether the station is active and should be synced")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Radio Station"
        verbose_name_plural = "Radio Stations"

    def __str__(self):
        return self.name
