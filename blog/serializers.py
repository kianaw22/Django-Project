
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
    

from rest_framework import serializers
from .models import CustomUser

class ChangeRoleSerializer(serializers.Serializer):
    """
    Serializer for updating a user's role.
    """
    user_id = serializers.IntegerField(required=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    def validate_user_id(self, value):
        """
        Ensure the user exists.
        """
        try:
            self.instance = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return value

    def update(self, instance, validated_data):
        """
        Update the role of the user.
        """
        instance.role = validated_data['role']
        instance.save()
        return instance

