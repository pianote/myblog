from rest_framework import serializers
from django.contrib.auth import password_validation
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
User = get_user_model()

# LOGIN
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)
# CREATE TOKEN (FOR RESPONSE DATA)
class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model = User
         fields = ('id', 'name', 'email', 'is_active', 'is_staff', 'auth_token')
         read_only_fields = ('id', 'is_active', 'is_staff')
    def get_auth_token(self, obj):
        refresh = RefreshToken.for_user(user=obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
# CREATE USER
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value



class UserProfileUpdateSerializer(serializers.Serializer):
    pass

class EmptySerializer(serializers.Serializer):
    pass