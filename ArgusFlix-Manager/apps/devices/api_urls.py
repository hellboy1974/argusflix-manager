from rest_framework.routers import DefaultRouter
from .api_views import ArgusDeviceViewSet, DeviceBackupViewSet

router = DefaultRouter()
router.register(r'devices', ArgusDeviceViewSet, basename='device')
router.register(r'backups', DeviceBackupViewSet, basename='device-backup')

urlpatterns = router.urls
