# apps/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('user_level', 10)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()
    """
    Custom user model for ArgusFlix.
    Inherits from Django's AbstractUser to add additional fields if needed.
    """

    class UserLevel(models.IntegerChoices):
        STREAMER = 0, "Streamer"
        STANDARD = 1, "Standard User"
        ADMIN = 10, "Admin"

    avatar_config = models.JSONField(default=dict, blank=True, null=True)
    channel_profiles = models.ManyToManyField(
        "argusflix_manager_channels.ChannelProfile",
        blank=True,
        related_name="users",
    )
    user_level = models.IntegerField(default=UserLevel.STREAMER)
    custom_properties = models.JSONField(default=dict, blank=True, null=True)
    api_key = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    stream_limit = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def get_groups(self):
        """
        Returns the groups (roles) the user belongs to.
        """
        return self.groups.all()

    def get_permissions(self):
        """
        Returns the permissions assigned to the user and their groups.
        """
        return self.user_permissions.all() | Permission.objects.filter(group__user=self)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=100)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True, help_text="Numeric PIN for profile protection")
    is_kids_profile = models.BooleanField(default=False)
    layout_profile = models.ForeignKey("appbuilder.AppProfile", on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_profiles", help_text="Custom UI Layout Profile")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class WatchHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='watch_history')
    content_type = models.CharField(max_length=50) # 'movie', 'series', 'live'
    content_id = models.CharField(max_length=100)
    progress_seconds = models.IntegerField(default=0)
    duration_seconds = models.IntegerField(default=0)
    last_watched = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('profile', 'content_type', 'content_id')

    def __str__(self):
        return f"{self.profile.name} - {self.content_type}:{self.content_id}"


class Favorite(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='favorites')
    content_type = models.CharField(max_length=50)
    content_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'content_type', 'content_id')

    def __str__(self):
        return f"{self.profile.name} favors {self.content_type}:{self.content_id}"
