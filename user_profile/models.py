from django.db import models
from django_resized import ResizedImageField


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, default='')
    last_online = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, blank=True, default='')
    photo = ResizedImageField(
        upload_to='profile-photos/',
        size=[300, 300],
        force_format='WEBP',
        quality=80,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username
