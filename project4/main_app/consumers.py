import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import CallRoom, CallParticipant


class VideoCallConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("WebSocket connect called!")

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'call_{self.room_id}'
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.add_participant()
        await self.accept()

        participants = await self.get_room_participants()

        await self.send(text_data=json.dumps({
            'type': 'users_in_room',
            'users': [p['user_id'] for p in participants]
        }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user_id': self.user.id,
                'username': self.user.username
            }
        )

    async def disconnect(self, close_code):
        await self.remove_participant()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'user_id': self.user.id,
                'username': self.user.username
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        # ======================
        # 🎥 WEBRTC SIGNALING
        # ======================
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

        # ======================
        # 💬 CHAT (GROUP + PRIVATE)
        # ======================
        elif message_type == 'chat_message':
            target = data.get('target')

            # 🔹 GROUP CHAT
            if target == 'all':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': data['message'],
                        'username': data['username'],
                        'user_id': self.user.id,
                    }
                )

            # 🔹 PRIVATE CHAT
            else:
                participants = await self.get_room_participants()

                for p in participants:
                    if str(p['user_id']) == str(target) and p.get('channel_name'):
                        await self.channel_layer.send(
                            p['channel_name'],
                            {
                                'type': 'chat_message',
                                'message': data['message'],
                                'username': data['username'],
                                'user_id': self.user.id,
                            }
                        )

                # send back to sender so they see it
                await self.send(text_data=json.dumps({
                    'type': 'chat_message',
                    'message': data['message'],
                    'username': data['username'],
                    'user_id': self.user.id,
                }))

        # ======================
        # 👥 PARTICIPANTS LIST
        # ======================
        elif message_type == 'get_participants':
            participants = await self.get_room_participants()

            await self.send(text_data=json.dumps({
                'type': 'participants_list',
                'participants': participants
            }))

    # ======================
    # 🔁 EVENTS TO CLIENT
    # ======================

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
        }))

    async def webrtc_offer(self, event):
        if event.get('target_id') and event['target_id'] != self.user.id:
            return 
        await self.send(text_data=json.dumps({
        'type': 'offer',
        'offer': event['offer'],
        'sender_id': event['sender_id']
    }))

        if event['sender_id'] != self.user.id:
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

    # ======================
    # 🗄 DATABASE
    # ======================

    @database_sync_to_async
    def add_participant(self):
        try:
            room = CallRoom.objects.get(room_id=self.room_id)

            participant, _ = CallParticipant.objects.get_or_create(
                room=room,
                user=self.user
            )

            participant.is_online = True
            participant.channel_name = self.channel_name  # 🔥 IMPORTANT
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
                    'username': p.user.username,
                    'channel_name': p.channel_name  
                }
                for p in participants
            ]

        except CallRoom.DoesNotExist:
            return []