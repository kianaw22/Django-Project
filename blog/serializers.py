
from rest_framework import serializers
from .models import Post,CustomUser
from django.contrib.auth.hashers import make_password

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields='__all__'
class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for signing up a CustomUser without password hashing.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)