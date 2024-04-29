from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from chat.models import ChatRoom, TextMessage
from django.db import models

from chat.serializers import ChatMessageSerializer, ChatRoomSerializer


@database_sync_to_async
def get_user_by_token(token):
    user_id = AccessToken(token)['user_id']
    user = User.objects.get(id=user_id)

    return user


@database_sync_to_async
def get_room(author_id, user_ids, group_id, name=''):
    if group_id:
        return ChatRoom.objects.get(id=group_id), False

    room, is_created = ChatRoom.objects.get_or_create(
        name=name if len(user_ids) > 1 else f'{author_id}-{user_ids[0]}',
        created_by_id=author_id,
    )
    room.members.add(*user_ids)
    room.save()

    return room, is_created


@database_sync_to_async
def create_room(author_id, user_ids, name) -> tuple[ChatRoom, ChatMessageSerializer | None]:
    user = User.objects.get(id=author_id)

    room, is_created = ChatRoom.objects.get_or_create(
        name=name if len(user_ids) > 1 else f'{user_ids[0]}',
        created_by=user,
    )

    room.members.add(*user_ids)
    room.save()

    message = None
    if not is_created:
        message = TextMessage.objects.create(
            user=user,
            text=f'Gurup {user.username} tarafından oluşturuldu!',
            room=room,
        )

    return room, ChatMessageSerializer(message) if message else None


@database_sync_to_async
def create_message(room: int, user: User, text: str) -> TextMessage:
    message = TextMessage.objects.create(
        user=user,
        text=text,
        room_id=room,
    )

    return ChatMessageSerializer(message).data


@database_sync_to_async
def get_users_from_room(room: ChatRoom):
    return [
        room.created_by.id,
        *room.members.values_list('id', flat=True)
    ]


@database_sync_to_async
def get_rooms_from_user(user: User):
    rooms = ChatRoom.objects.filter(
        models.Q(created_by=user) | models.Q(members__in=[user])
    ).values_list('pk', flat=True)

    return list(rooms)
