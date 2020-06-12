from rest_framework import serializers
from django.contrib.auth import password_validation
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from .models import UserProfile
User = get_user_model()

# LOGIN
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

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

# CHANGE PASSWORD
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

# RESET PASSWORD
# class PasswordResetSerializer(serializers.Serializer):
#     uid = serializers.CharField(required=True)
#     token = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)
#     re_new_password = serializers.CharField(required=True)
    
# UPDATE PROFILE
class UserProfileUpdateSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ('image','bio')

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance

### READ ONLY
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     url = serializers.HyperlinkedIdentityField(view_name='users:user-detail')

#     class Meta:
#         model = User
#         fields = ['id', 'url', 'name', 'email']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['user','image','bio']

class EmptySerializer(serializers.Serializer):
    pass