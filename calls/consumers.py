# calls/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_user_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        self.room_name = f"call_{min(self.user.id, int(self.other_user_id))}_{max(self.user.id, int(self.other_user_id))}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        logger.info(f"{self.user.username} connected to room {self.room_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        # Notify other user
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "call.message",
                "message": {"callEnded": True},
                "sender_channel": self.channel_name
            }
        )
        logger.info(f"{self.user.username} disconnected from room {self.room_name}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        logger.info(f"Received WS data from {self.user.username}: {data}")
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "call.message",
                "message": data,
                "sender_channel": self.channel_name
            }
        )

    async def call_message(self, event):
        message = event["message"]
        sender = event["sender_channel"]
        if self.channel_name != sender:
            await self.send(text_data=json.dumps(message))
