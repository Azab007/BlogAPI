from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username','password', 'email', 'first_name', 'last_name')
        ref_name='UserSerializer'
