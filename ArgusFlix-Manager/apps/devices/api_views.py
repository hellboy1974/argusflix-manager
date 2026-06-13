import random
import subprocess
import os
import urllib.request
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
    def remote_install(self, request):
        ip = request.data.get('ip')
        if not ip:
            return Response({'error': 'IP address is required'}, status=400)
            
        try:
            # 1. Connect via ADB
            connect_res = subprocess.run(['adb', 'connect', ip], capture_output=True, text=True, timeout=10)
            if 'connected' not in connect_res.stdout.lower() and 'already connected' not in connect_res.stdout.lower():
                return Response({'error': f'Failed to connect to {ip}: {connect_res.stdout}'}, status=400)
                
            # 2. Download APK temporarily
            apk_path = '/tmp/ArgusFlix.apk'
            if not os.path.exists(apk_path):
                apk_url = 'https://github.com/Davidona/ArgusFlix-IPTV/releases/latest/download/ArgusFlix.apk'
                urllib.request.urlretrieve(apk_url, apk_path)
                
            # 3. Install APK
            install_res = subprocess.run(['adb', '-s', ip, 'install', '-r', apk_path], capture_output=True, text=True, timeout=60)
            if 'Success' not in install_res.stdout:
                return Response({'error': f'Failed to install APK: {install_res.stdout}\n{install_res.stderr}'}, status=400)
                
            # 4. Launch App
            subprocess.run(['adb', '-s', ip, 'shell', 'monkey', '-p', 'com.argusflix.app', '-c', 'android.intent.category.LAUNCHER', '1'], capture_output=True)
            
            return Response({'status': 'success', 'message': 'App installed and launched successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        finally:
            subprocess.run(['adb', 'disconnect', ip], capture_output=True)

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

    def create(self, request, *args, **kwargs):
        device_id_str = request.data.get('device_id')
        if device_id_str:
            try:
                device = ArgusDevice.objects.get(device_id=device_id_str)
                # Mutate the POST data to include the actual PK
                request.data['device'] = device.pk
            except ArgusDevice.DoesNotExist:
                return Response({'error': 'Device not found'}, status=404)
        return super().create(request, *args, **kwargs)

class KeymapProfileViewSet(viewsets.ModelViewSet):
    from .models import KeymapProfile
    from .serializers import KeymapProfileSerializer
    queryset = KeymapProfile.objects.all().order_by('-created_at')
    serializer_class = KeymapProfileSerializer
