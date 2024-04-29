from django.urls import path
from .viewsets import get_chat_rooms

urlpatterns = [
    path('get_rooms/', get_chat_rooms),
]