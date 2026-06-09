import random
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ArgusDevice, DeviceBackup
from .serializers import ArgusDeviceSerializer, DeviceBackupSerializer

class ArgusDeviceViewSet(viewsets.ModelViewSet):
    queryset = ArgusDevice.objects.all().order_by('-created_at')
    serializer_class = ArgusDeviceSerializer

    @action(detail=False, methods=['post'])
    def generate_pairing_code(self, request):
        # Generate a random 6-digit code
        code = str(random.randint(100000, 999999))
        while ArgusDevice.objects.filter(pairing_code=code).exists():
            code = str(random.randint(100000, 999999))
        
        device = ArgusDevice.objects.create(pairing_code=code, device_id=f"pending_{code}")
        return Response({'pairing_code': code, 'id': device.id})

    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    def pair(self, request):
        pairing_code = request.data.get('pairing_code')
        device_id = request.data.get('device_id')
        name = request.data.get('name', 'Unknown TV')

        if not pairing_code or not device_id:
            return Response({'error': 'pairing_code and device_id required'}, status=400)

        try:
            device = ArgusDevice.objects.get(pairing_code=pairing_code)
            device.device_id = device_id
            device.name = name
            device.is_paired = True
            device.pairing_code = None # Clear code after pairing
            
            # Get IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            device.last_ip = ip
            device.save()
            
            return Response({'status': 'success', 'message': 'Device paired successfully'})
        except ArgusDevice.DoesNotExist:
            return Response({'error': 'Invalid pairing code'}, status=404)

    @action(detail=True, methods=['post'])
    def send_command(self, request, pk=None):
        device = self.get_object()
        command = request.data.get('command')
        payload = request.data.get('payload', {})

        if not command:
            return Response({'error': 'command required'}, status=400)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'device_{device.device_id}',
            {
                'type': 'device_command',
                'command': command,
                'payload': payload
            }
        )
        return Response({'status': 'success', 'message': 'Command sent to device'})

class DeviceBackupViewSet(viewsets.ModelViewSet):
    queryset = DeviceBackup.objects.all().order_by('-created_at')
    serializer_class = DeviceBackupSerializer
