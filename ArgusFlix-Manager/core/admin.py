# core/admin.py

from django.contrib import admin
from .models import UserAgent, StreamProfile, CoreSettings, AppMenuSection

@admin.register(UserAgent)
class UserAgentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user_agent",
        "description",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "user_agent", "description")
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")

@admin.register(StreamProfile)
class StreamProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "command",
        "is_active",
        "user_agent",
    )
    search_fields = ("name", "command", "user_agent")
    list_filter = ("is_active",)

@admin.register(CoreSettings)
class CoreSettingsAdmin(admin.ModelAdmin):
    """
    Because CoreSettings is typically a single 'singleton' row,
    you can either allow multiple or restrict it. For now, we
    just list and allow editing of any instance.
    """
    list_display = (
        "key",
        "value",
    )

@admin.register(AppMenuSection)
class AppMenuSectionAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "internal_id",
        "sort_order",
        "is_visible",
    )
    search_fields = ("label", "internal_id")
    list_filter = ("is_visible",)
    ordering = ("sort_order", "label")

from .models import DeviceCommand, DeviceBackup

@admin.register(DeviceCommand)
class DeviceCommandAdmin(admin.ModelAdmin):
    list_display = ('command_type', 'device_id', 'status', 'created_at')
    list_filter = ('command_type', 'status')
    search_fields = ('device_id',)

@admin.register(DeviceBackup)
class DeviceBackupAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'device_name', 'file_size', 'created_at')
    search_fields = ('device_id', 'device_name', 'included_content')
from .models import AppPageLayout

@admin.register(AppPageLayout)
class AppPageLayoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'page', 'section_type', 'content_source', 'sort_order', 'is_active')
    list_filter = ('page', 'section_type', 'content_source', 'is_active')
    search_fields = ('title', 'provider_id', 'category_id')
    ordering = ('page', 'sort_order')
