from rest_framework import serializers
from .models import ArgusDevice, DeviceBackup, KeymapProfile

class KeymapProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeymapProfile
        fields = '__all__'

class ArgusDeviceSerializer(serializers.ModelSerializer):
    keymap_data = KeymapProfileSerializer(source='keymap', read_only=True)

    class Meta:
        model = ArgusDevice
        fields = '__all__'
        read_only_fields = ['is_paired', 'last_ip', 'last_seen']

class DeviceBackupSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = DeviceBackup
        fields = '__all__'
