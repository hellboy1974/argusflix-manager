from django.db import models

class AppProfile(models.Model):
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AppPage(models.Model):
    PAGE_TYPES = (
        ('home', 'Home Screen'),
        ('movies', 'Movies'),
        ('series', 'Series'),
        ('live_tv', 'Live TV'),
    )
    profile = models.ForeignKey(AppProfile, related_name='pages', on_delete=models.CASCADE)
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES)
    title = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('profile', 'page_type')

    def __str__(self):
        return f"{self.profile.name} - {self.get_page_type_display()}"

class AppWidget(models.Model):
    WIDGET_TYPES = (
        ('hero', 'Hero Banner'),
        ('continue_watching', 'Continue Watching'),
        ('category_row', 'Category Row'),
        ('trending', 'Trending / Popular'),
        ('recent_live_tv', 'Recent Live TV'),
        ('recently_added', 'Recently Added (Per Server)'),
        ('now_playing', 'Now Playing / EPG Live'),
        ('favorites', 'Favorites'),
        ('custom_banner', 'Custom Banner / Announcement'),
    )
    page = models.ForeignKey(AppPage, related_name='widgets', on_delete=models.CASCADE)
    widget_type = models.CharField(max_length=30, choices=WIDGET_TYPES)
    order = models.PositiveIntegerField(default=0)
    settings = models.JSONField(default=dict, blank=True, help_text="Specific settings for this widget, e.g., category ID, server ID, or banner text.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_widget_type_display()} ({self.page})"
