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
    email = serializers.EmailField(required=False, default='')

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'bio', 'photo', 'first_name', 'last_name', 'email')

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.user.first_name = self.validated_data['first_name']
        instance.user.last_name = self.validated_data['last_name']
        instance.user.email = self.validated_data['email']
        instance.user.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    user = UserCreateProfileSerializer()

    class Meta:
        model = UserProfile
        fields = ('user', "phone_number", 'photo', 'bio',)


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('password', 'new_password')

    def save(self, **kwargs):
        if not self.instance.check_password(self.validated_data['password']):
            raise serializers.ValidationError({'password': 'Wrong password.'})
        self.instance.set_password(self.validated_data['new_password'])
        self.instance.save()
        return self.instance
