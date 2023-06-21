from django.shortcuts import render
from rest_framework import generics,authentication,permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (UserSerializers,AuthTokenSerializer)

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializers
    

class CreateTokenView(ObtainAuthToken):
    '''create a new auth token for user'''
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        '''Retrive and return the authenticated user'''
        return self.request.user


      