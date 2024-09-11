# django
from django.conf import settings

# channels
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# other
import json


class myAsyncJsonConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        try:
            self.room_group_name = settings.SOCKET_CHANNEL_NAME
            
            # Join room group

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        except Exception as e:
            await self.close()

    
    async def disconnect(self, code):
        
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            await self.close()

    async def entry_deleted(self, event):
        message = event['message']
        entry_id = event['entry_id']
        type = event['type']
        await self.send(text_data=json.dumps({
            "event": type,
            "entry_id": entry_id,
            "message": message
        }))