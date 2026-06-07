import uuid
from django.db import models

class ArgusDevice(models.Model):
    device_id = models.CharField(max_length=255, unique=True, help_text="Unique identifier from the TV app")
    name = models.CharField(max_length=255, default="Unnamed TV")
    pairing_code = models.CharField(max_length=6, blank=True, null=True, unique=True)
    is_paired = models.BooleanField(default=False)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.device_id})"

class DeviceBackup(models.Model):
    device = models.ForeignKey(ArgusDevice, on_delete=models.CASCADE, related_name="backups")
    file = models.FileField(upload_to="device_backups/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Backup for {self.device.name} at {self.created_at}"
