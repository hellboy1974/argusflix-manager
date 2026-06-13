from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import AppWidget, AppPage
try:
    from apps.devices.models import ArgusDevice
except ImportError:
    ArgusDevice = None

def push_layout_update(page):
    if not ArgusDevice:
        return
        
    channel_layer = get_channel_layer()
    if not channel_layer:
        return
        
    devices = ArgusDevice.objects.all()
    for device in devices:
        async_to_sync(channel_layer.group_send)(
            f'device_{device.id}',
            {
                'type': 'device_command',
                'command': 'SYNC_LAYOUTS',
                'payload': {
                    'profile_id': page.profile.id,
                    'page_type': page.page_type
                }
            }
        )

@receiver(post_save, sender=AppWidget)
@receiver(post_delete, sender=AppWidget)
def widget_updated(sender, instance, **kwargs):
    push_layout_update(instance.page)

@receiver(post_save, sender=AppPage)
def page_updated(sender, instance, **kwargs):
    push_layout_update(instance)
