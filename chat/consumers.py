from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .registry import registry
from django.utils import timezone
from .utils import get_user_by_token, get_room, get_message, get_rooms_from_user, create_room


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def authenticate(self):
        try:
            token = next(filter(lambda x: str(x[0].decode('utf-8')) == 'token', self.scope['headers']))[-1]
            self.scope['user'] = await get_user_by_token(token)
            return True
        except Exception:
            pass

        await self.send_json(
            {'status': 'error', 'message': 'Authentication failed'},
        )
        await self.close()
        await self.disconnect(0)

    async def group_message(self, event):
        await self.send_json(event)

    async def broadcast(self, room, message):
        await self.channel_layer.group_send(str(room.id), {
            'type': 'group_message',
            'message': message
        })

    async def connect(self):
        await self.accept()

        is_authenticated = await self.authenticate()

        if not is_authenticated:
            return

        registry.add_channel_for_user(self.scope['user'].id, self.channel_name)
        room_ids = await get_rooms_from_user(self.scope['user'])

        for room_id in room_ids:
            await self.channel_layer.group_add(str(room_id), self.channel_name)

    async def disconnect(self, close_code):
        room_ids = await get_rooms_from_user(self.scope['user'])

        for room_id in room_ids:
            await self.channel_layer.group_discard(str(room_id), self.channel_name)

        registry.remove_channel_for_user(self.scope['user'].id)
        self.scope['user'].profile.last_online = timezone.now()
        self.scope['user'].profile.save()
        self.scope['user'] = None

    async def add_other_users_to_group(self, user_ids, room_id):
        await self.channel_layer.group_add(room_id, self.channel_name)

        for user_id in user_ids:
            channel_name = registry.get_channel_for_user(user_id)
            channel_name and await self.channel_layer.group_add(room_id, registry.get_channel_for_user(user_id))

    async def on_create_room(self, content):
        user_ids, name = content.get('user_ids', None), content.get('name', None)

        room, message = await create_room(self.scope['user'].id, user_ids, name)
        await self.channel_layer.group_add(str(room.id), self.channel_name)

        for user_id in user_ids:
            channel_name = registry.get_channel_for_user(user_id)
            await self.channel_layer.group_add(str(room.id), channel_name)

        message = message.data
        await self.broadcast(room, message)

    async def on_message(self, content):
        pass

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')

        if message_type == 'create_room':
            await self.on_create_room(content)
