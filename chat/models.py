from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField


class ChatRoom(models.Model):
    photo = ResizedImageField(
        upload_to='chat-room-photos/',
        size=[500, 500],
        force_format='WEBP',
        quality=80,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='members')


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.ManyToManyField(User, related_name='%(class)ss_read')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='%(class)ss_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TextMessage(Message):
    GROUP_CREATED = 'group_created'
    MESSAGE = 'message'

    type = models.CharField(max_length=255, choices=[(GROUP_CREATED, GROUP_CREATED), (MESSAGE, MESSAGE)])
    text = models.TextField()


class ImageMessage(Message):
    image = ResizedImageField(
        upload_to='images/',
        size=[500, 500],
        force_format='WEBP',
        quality=80,
    )


class FileMessage(Message):
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.file.name
