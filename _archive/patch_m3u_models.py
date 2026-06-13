# -*- coding: utf-8 -*-
import re

file_path = 'ArgusFlix-Manager/apps/m3u/models.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'sync_policy = models.CharField' not in content:
    # Add SyncPolicy text choices
    sync_choices = '''
    class SyncPolicy(models.TextChoices):
        AUTO_ON_STARTUP = "auto_on_startup", "Beim Starten"
        MANUAL = "manual", "Nur Manuell"
'''
    
    # Insert SyncPolicy choices before Status
    content = content.replace('    class Status(models.TextChoices):', sync_choices + '\n    class Status(models.TextChoices):')
    
    fields = '''
    sync_policy = models.CharField(
        max_length=20, choices=SyncPolicy.choices, default=SyncPolicy.MANUAL,
        help_text="Synchronisations-Richtlinie"
    )
    sync_with_devices = models.BooleanField(
        default=True, help_text="Synchronisation mit angebundenen Apps/Geräten zulassen"
    )
'''
    # Insert fields after 'is_active'
    content = content.replace(
        'is_active = models.BooleanField(\n        default=True, help_text="Set to false to deactivate this M3U account"\n    )',
        'is_active = models.BooleanField(\n        default=True, help_text="Set to false to deactivate this M3U account"\n    )' + fields
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print("M3UAccount patched.")
