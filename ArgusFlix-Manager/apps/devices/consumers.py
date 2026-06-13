import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DeviceWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.room_group_name = f'device_{self.device_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            action = data.get('action')
            
            if action == 'update_progress':
                # Use sync_to_async since we are doing DB operations
                from asgiref.sync import sync_to_async
                from apps.accounts.models import Profile, WatchHistory
                from django.utils import timezone
                
                profile_id = data.get('profile_id')
                content_type = data.get('content_type')
                content_id = str(data.get('content_id', ''))
                progress = int(data.get('progress', 0))
                duration = int(data.get('duration', 0))
                
                if profile_id and content_type and content_id:
                    @sync_to_async
                    def update_history():
                        try:
                            profile = Profile.objects.get(id=profile_id)
                            completed = False
                            if duration > 0 and progress >= (duration * 0.9):
                                completed = True
                            
                            WatchHistory.objects.update_or_create(
                                profile=profile,
                                content_type=content_type,
                                content_id=content_id,
                                defaults={
                                    'progress_seconds': progress,
                                    'duration_seconds': duration,
                                    'completed': completed,
                                    'last_watched': timezone.now()
                                }
                            )
                        except Profile.DoesNotExist:
                            pass
                            
                    await update_history()
                    
        except Exception as e:
            pass

    async def device_command(self, event):
        command = event['command']
        payload = event.get('payload', {})

        await self.send(text_data=json.dumps({
            'command': command,
            'payload': payload
        }))
