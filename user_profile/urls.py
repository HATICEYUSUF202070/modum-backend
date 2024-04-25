from django.urls import path
from .viewsets import create_user_profile, edit_user_profile, get_user_profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('create/', create_user_profile),
    path('edit/', edit_user_profile),
    path('profile/', get_user_profile),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
