from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from chat.models import ChatRoom
from chat.serializers import ChatRoomSerializer


# Create your views here.

@api_view(['GET'])
def get_chat_rooms(request):
    chat_rooms = ChatRoom.objects.all()
    serializer = ChatRoomSerializer(chat_rooms, many=True)
    return Response(serializer.data)
