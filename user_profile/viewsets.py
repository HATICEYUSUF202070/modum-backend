from rest_framework.decorators import api_view
from .serializers import UserCreateProfileSerializer, UserEditProfileSerializer, UserSerializer, \
    ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile


@api_view(['POST'])
def create_user_profile(request):
    serializer = UserCreateProfileSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        UserProfile.objects.create(user=instance)
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_user_profile(request):
    serializer = UserEditProfileSerializer(instance=request.user.profile, data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_profile(request):
    serializer = UserSerializer(instance=request.user.profile)
    return Response(serializer.data)


@api_view(['POST'])
def change_password(request):
    serializer = ChangePasswordSerializer(instance=request.user, data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
