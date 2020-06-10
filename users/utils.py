from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()

def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is None:
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    return user

def create_user_account(email, password, name, **kwargs):
    user = User.objects.create_user(email=email, password=password, name=name, **kwargs)
    return user