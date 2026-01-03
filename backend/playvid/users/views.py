from django.shortcuts import render, get_object_or_404
from users.models import CustomUser, Channel
from users.serializers import UserSerializer, ChannelSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def check_auth(request, instance):
        """
        Check auth and check which user to join in site.
        If user will be try change other user then get error
        In this function return bool type.
        """
        if ((not request.user and request.user.is_authenticated)
            or (request.user and request.user.is_staff)):
            return False
        if not instance == request.user or request.user.is_staff:
            return False
        return True


class UsersListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class UserView(generics.RetrieveUpdateDestroyAPIView):
    """
    This API can be change data or check data users separately.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = 'user_id'
    
    
    def get_permissions(self):
        """
        Check on the users can all,
        since change data should only owner.
        """
        self.permission_classes = [AllowAny]
        
        if self.request.method in {'POST', 'PUT', 'DELETE', 'PATCH'}:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    
    def get(self, request, *args, **kwargs):
        """
        If server not found user then give error or
        give data about user.
        """
        user_id = kwargs.get('user_id')
        instance = get_object_or_404(CustomUser, pk=user_id)
        serializer_data = UserSerializer(instance)
        
        return Response(serializer_data.data)
    
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if not check_auth(request, instance):
            return Response({
                    'detail': 'You do not have permission to perform this action.'
                }, status=status.HTTP_403_FORBIDDEN)
            
        return super().delete(request, *args, **kwargs)
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not check_auth(request, instance):
            return Response({
                    'detail': 'You do not have permission to perform this action.'
                }, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)


class ChannelListView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny]


class ChannelView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_url_kwarg = 'channel_id'
    
    
    def get_permissions(self):
        """
        Check on the users can all,
        since change data should only owner.
        """
        self.permission_classes = [AllowAny]
        
        if self.request.method in {'POST', 'PUT', 'DELETE', 'PATCH'}:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if not check_auth(request, instance):
            return Response({
                    'detail': 'You do not have permission to perform this action.'
                }, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not check_auth(request, instance):
            return Response({
                    'detail': 'You do not have permission to perform this action.'
                }, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)