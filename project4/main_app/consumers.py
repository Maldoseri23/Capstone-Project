import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import CallRoom, CallParticipant

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'call_{self.room_id}'
        self.user = self.scope['user']
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Add user to room participants
        await self.add_participant()
        
        await self.accept()
        
        # Notify others that user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user_id': self.user.id,
                'username': self.user.username
            }
        )

    async def disconnect(self, close_code):
        # Remove user from room participants
        await self.remove_participant()
        
        # Notify others that user left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'user_id': self.user.id,
                'username': self.user.username
            }
        )
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'offer':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_offer',
                    'offer': data['offer'],
                    'sender_id': self.user.id,
                    'target_id': data.get('target_id')
                }
            )
        elif message_type == 'answer':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'webrtc_answer',
                    'answer': data['answer'],
                    'sender_id': self.user.id,
                    'target_id': data.get('target_id')
                }
            )
        elif message_type == 'ice_candidate':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ice_candidate',
                    'candidate': data['candidate'],
                    'sender_id': self.user.id,
                    'target_id': data.get('target_id')
                }
            )
        elif message_type == 'get_participants':
            participants = await self.get_room_participants()
            await self.send(text_data=json.dumps({
                'type': 'participants_list',
                'participants': participants
            }))

    # WebRTC signaling message handlers
    async def webrtc_offer(self, event):
        # Send offer to specific user or broadcast if no target
        if event.get('target_id') and event['target_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'offer',
                'offer': event['offer'],
                'sender_id': event['sender_id']
            }))
        elif not event.get('target_id') and event['sender_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'offer',
                'offer': event['offer'],
                'sender_id': event['sender_id']
            }))

    async def webrtc_answer(self, event):
        if event.get('target_id') == self.user.id or event['sender_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'answer',
                'answer': event['answer'],
                'sender_id': event['sender_id']
            }))

    async def ice_candidate(self, event):
        if event['sender_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'ice_candidate',
                'candidate': event['candidate'],
                'sender_id': event['sender_id']
            }))

    async def user_joined(self, event):
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'user_joined',
                'user_id': event['user_id'],
                'username': event['username']
            }))

    async def user_left(self, event):
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'user_left',
                'user_id': event['user_id'],
                'username': event['username']
            }))

    @database_sync_to_async
    def add_participant(self):
        try:
            room = CallRoom.objects.get(room_id=self.room_id)
            participant, created = CallParticipant.objects.get_or_create(
                room=room,
                user=self.user,
                defaults={'is_online': True}
            )
            if not created:
                participant.is_online = True
                participant.save()
        except CallRoom.DoesNotExist:
            pass

    @database_sync_to_async
    def remove_participant(self):
        try:
            room = CallRoom.objects.get(room_id=self.room_id)
            participant = CallParticipant.objects.get(room=room, user=self.user)
            participant.is_online = False
            participant.save()
        except (CallRoom.DoesNotExist, CallParticipant.DoesNotExist):
            pass

    @database_sync_to_async
    def get_room_participants(self):
        try:
            room = CallRoom.objects.get(room_id=self.room_id)
            participants = CallParticipant.objects.filter(
                room=room, 
                is_online=True
            ).select_related('user')
            return [
                {
                    'user_id': p.user.id,
                    'username': p.user.username
                } 
                for p in participants
            ]
        except CallRoom.DoesNotExist:
            return []