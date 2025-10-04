from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage, WorkSpace
import json
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.workspace_id = self.scope['url_route']['kwargs']['workspace_id']
        self.room_group_name = f"workspace_{self.workspace_id}"

        # add user to the workspace group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # history of chat
        past_messages = await self.get_past_messages(self.workspace_id)
        
        messages_data = [
            {
                'sender': msg.sender.username,
                'message': msg.message,
                'created_at': str(msg.created_at)
            }
            for msg in past_messages
        ]
        
        await self.send(text_data=json.dumps({
            'type': 'past_messages',
            'messages': messages_data
        }))

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    
    # Receive message from WebSocket
    async def receive(self, text_data = None, bytes_data = None):
        data = json.loads(text_data)       
        message = data['message']
        sender = self.scope['user']

        # Save message to DB
        await self.save_message(sender, message)

        # Broadcast message to workspace group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', # this will must match with handler method --> chat_message
                'message': message,
                'sender': sender.username
            }
        )

    
    # Receives message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # send message to websocket
        await self.send(
            text_data = json.dumps({
                'sender': sender,
                'message': message
            })
        )

    @sync_to_async
    def save_message(self, sender, message):
        "Persist chat message into DB"
        workspace = WorkSpace.objects.get(id=self.workspace_id)
        return ChatMessage.objects.create(
            workspace=workspace,
            sender=sender,
            message=message
        )   
    
    @sync_to_async
    def get_past_messages(self, workspace_id):
        return ChatMessage.objects.filter(workspace_id=workspace_id).order_by('created_at')[:50]