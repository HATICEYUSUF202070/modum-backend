from rest_framework import serializers
from django.contrib.auth.models import User

from user_profile.models import UserProfile


class UserCreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserEditProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, default='')
    last_name = serializers.CharField(required=False, default='')

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'bio', 'photo', 'first_name', 'last_name')

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.user.first_name = self.validated_data['first_name']
        instance.user.last_name = self.validated_data['last_name']
        instance.user.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    user = UserCreateProfileSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', "phone_number", 'photo', 'bio')


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    fields = ('old_password', 'new_password')

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        if not instance.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})
        instance.set_password(self.validated_data['new_password'])
        instance.save()
        return instance
