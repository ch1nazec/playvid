from django.shortcuts import render
from users.models import CustomUser, Channel
from users.serializers import UserSerializer, ChannelSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated


# Create your views here.
class UserView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    


class ChannelView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny]