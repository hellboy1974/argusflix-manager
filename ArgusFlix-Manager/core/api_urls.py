# core/api_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    UserAgentViewSet,
    StreamProfileViewSet,
    OutputProfileViewSet,
    CoreSettingsViewSet,
    SystemNotificationViewSet,
    environment,
    version,
    rehash_streams_endpoint,
    TimezoneListView,
    get_system_events,
    get_active_connections,
    kill_active_connection,
    get_vpn_status,
    provider_audit_endpoint,
    clear_system_cache,
    proxy_doctor_scan,
    proxy_doctor_clean,
    AppMenuSectionViewSet,
    DeviceCommandViewSet,
    DeviceBackupViewSet,
    AppPageLayoutViewSet,
    AppSettingsViewSet,
    MetadataProviderViewSet
)
from .api_tmdb import TmdbProxyView

router = DefaultRouter()
router.register(r'useragents', UserAgentViewSet, basename='useragent')
router.register(r'streamprofiles', StreamProfileViewSet, basename='streamprofile')
router.register(r'outputprofiles', OutputProfileViewSet, basename='outputprofile')
router.register(r'settings', CoreSettingsViewSet, basename='coresettings')
router.register(r'app-settings', AppSettingsViewSet, basename='appsettings')
router.register(r'notifications', SystemNotificationViewSet, basename='systemnotification')
router.register(r'app-menu', AppMenuSectionViewSet, basename='appmenusection')
router.register(r'device-commands', DeviceCommandViewSet, basename='devicecommand')
router.register(r'device-backups', DeviceBackupViewSet, basename='devicebackup')
router.register(r'app-page-layouts', AppPageLayoutViewSet, basename='apppagelayout')
router.register(r'metadata-providers', MetadataProviderViewSet, basename='metadataprovider')

urlpatterns = [
    path('settings/env/', environment, name='token_refresh'),
    path('version/', version, name='version'),
    path('rehash-streams/', rehash_streams_endpoint, name='rehash_streams'),
    path('timezones/', TimezoneListView.as_view(), name='timezones'),
    path('system-events/', get_system_events, name='system_events'),
    path('admin/connections/', get_active_connections, name='admin-connections'),
    path('admin/connections/<str:client_id>/kill/', kill_active_connection, name='admin-kill-connection'),
    path('admin/vpn-status/', get_vpn_status, name='vpn-status'),
    path('admin/provider-audit/', provider_audit_endpoint, name='provider-audit'),
    path('admin/clear-cache/', clear_system_cache, name='clear-cache'),
    path('admin/proxy-doctor/scan/', proxy_doctor_scan, name='proxy-doctor-scan'),
    path('admin/proxy-doctor/clean/', proxy_doctor_clean, name='proxy-doctor-clean'),
    path('tmdb/<path:path>', TmdbProxyView.as_view(), name='tmdb_proxy'),
    path('', include(router.urls)),
]
