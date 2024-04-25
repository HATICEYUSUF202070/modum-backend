from rest_framework import serializers

from .models import ChatRoom, TextMessage, ImageMessage, FileMessage


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessage
        fields = ['user', 'room', 'text', 'id', 'created_at']
