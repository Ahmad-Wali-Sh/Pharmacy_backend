from rest_framework import serializers
from core.user_models import User  # Use your custom User model if applicable

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'image']