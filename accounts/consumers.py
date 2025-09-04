# accounts/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.caller_id = self.scope["url_route"]["kwargs"]["caller_id"]
        self.receiver_id = self.scope["url_route"]["kwargs"]["receiver_id"]

        # Create unique room for these two users
        ids = sorted([self.caller_id, self.receiver_id])
        self.room_name = f"call_{ids[0]}_{ids[1]}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Broadcast signaling data to the room
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "signal_message",
                "message": data
            }
        )

    async def signal_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))
