from django.contrib.auth import get_user_model, logout, login
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from . import serializers
from .models import UserProfile
from .utils import get_and_authenticate_user, create_user_account
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This "ReadOnlyModelViewSet" viewset automatically provides `list` and `detail` actions.
#     """
#     permission_classes = [AllowAny, ]
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer

class ProfileAPIView(RetrieveAPIView):
    """
    Provides get, put and patch method handlers.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = serializers.ProfileSerializer

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer,
        'logout': serializers.EmptySerializer,
        'password_change': serializers.PasswordChangeSerializer,
        'profile_update': serializers.UserProfileUpdateSerializer,
        'refresh': TokenRefreshSerializer,
    }
    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    # LOGIN VIEW    
    @action(methods=['POST', 'GET'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        token_serializer = TokenObtainPairSerializer(data=serializer.validated_data)
        token_serializer.is_valid(raise_exception=True) #create and add send new tokens
        data = token_serializer.validated_data
        return Response(data=data, status=status.HTTP_200_OK)

    # REGISTER VIEW
    @action(methods=['POST', 'GET'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        token_serializer = TokenObtainPairSerializer(data=serializer.validated_data)
        token_serializer.is_valid(raise_exception=True) #create and add send new tokens
        data = token_serializer.validated_data
        return Response(data=data, status=status.HTTP_201_CREATED)

    # LOGOUT VIEW (Authenticated user only)
    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ]) #Set Default in settings already
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    #CHANGE PASSWORD VIEW (Authenticated user only)
    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        data = {'success': 'Sucessfully updated password'}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

    #PROFILE UPDATE VIEW:
    @action(methods=['PUT'], detail=False, permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def profile_update(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(profile, serializer.validated_data)
        data = {'success': 'Sucessfully updated profile'}
        return Response(data=data, status=status.HTTP_200_OK)

    #REFRESH TOKEN
    @action(methods=['POST'], detail=False, permission_classes=[AllowAny, ])
    def refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data=data, status=status.HTTP_200_OK)

import os
import requests
from requests.auth import HTTPBasicAuth
from django.shortcuts import render, redirect
from django.http import HttpResponse

def password_reset_view(request, uid, token):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        re_new_password = request.POST.get('re_new_password')
        url = 'http://127.0.0.1:8000/users/reset_password_confirm/'
        body = {"new_password" : "%s" % new_password, "re_new_password" : "%s" % re_new_password, "uid": "%s" % uid, "token": "%s" % token}       
        print(body)
        requests.post(url, headers={'Content-Type': 'application/json'}, json=body)
        return HttpResponse('<h1>Password Reset Succesfully</h1>')
    else:
        return render(request, 'reset_password.html')
