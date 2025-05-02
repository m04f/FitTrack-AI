from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserInfoSerializer
from .models import UserInfo

class UserInfoView(generics.RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        userinfo, _ = UserInfo.objects.get_or_create(user=self.request.user)
        return userinfo

    def get_queryset(self):
        return UserInfo.objects.filter(user=self.request.user)
