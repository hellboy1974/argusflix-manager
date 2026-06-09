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
        # Here we could handle messages FROM the TV to ArgusFlix
        pass

    async def device_command(self, event):
        command = event['command']
        payload = event.get('payload', {})

        await self.send(text_data=json.dumps({
            'command': command,
            'payload': payload
        }))
