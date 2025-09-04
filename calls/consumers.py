from channels.generic.websocket import AsyncWebsocketConsumer
import json
#call/consumers.py

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract user IDs from URL
        caller_id = self.scope['url_route']['kwargs']['caller_id']
        receiver_id = self.scope['url_route']['kwargs']['receiver_id']

        # Create a consistent room name regardless of who initiates
        user_ids = sorted([int(caller_id), int(receiver_id)])
        self.room_name = f"call_{user_ids[0]}_{user_ids[1]}"

        # Store user info for this connection
        self.user_id = self.scope['user'].id if self.scope['user'].is_authenticated else None

        # Join room group
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        print(f"User {self.user_id} joined call room {self.room_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        print(f"User {self.user_id} left call room {self.room_name}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            # Add sender info to the message
            data['sender_id'] = self.user_id

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "call_message",
                    "message": data
                }
            )
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")

    async def call_message(self, event):
        message = event["message"]

        # Don't send the message back to the sender
        if message.get('sender_id') != self.user_id:
            await self.send(text_data=json.dumps(message))