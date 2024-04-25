from django.contrib import admin
from .models import ChatRoom, TextMessage, ImageMessage, FileMessage

admin.site.register(ChatRoom)
admin.site.register(TextMessage)
admin.site.register(ImageMessage)
admin.site.register(FileMessage)
