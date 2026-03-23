import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message,Room

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # ✅ MUST happen before accept()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': 'You are now connected',
            'author': 'System',
            'timestamp': ''
        }))

    async def receive(self, text_data):
        try:                                        # ✅ wrap in try/except
            text = json.loads(text_data)
            message = text['message']
            author = text['author']

            msg = await self.save_message(author, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': msg.message,
                    'author': msg.author.username,
                    'timestamp': str(msg.timestamp),
                }
            )

        except Exception as e:
            print(f"Error in receive: {e}")         # ✅ see exact error in terminal
            # send error back to browser instead of silently crashing
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Error: {str(e)}'
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'author': event['author'],
            'timestamp': event['timestamp'],
        }))

    async def disconnect(self, close_code):
        print(f"Disconnected with code: {close_code}")   # ✅ see close code in terminal
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, author, message):
       user, _ = User.objects.get_or_create(username=author)
       room, _ = Room.objects.get_or_create(room_name=self.room_name)  # ✅ get the Room object
       return Message.objects.create(
        author=user,
        message=message,
        room=room        # ✅ pass the object, not the string
    )