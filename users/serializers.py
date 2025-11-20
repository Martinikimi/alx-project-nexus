from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_one = True
        min_length = 8
        error_messages = {'min length': 'Password must be atleast eight characters'}
    )
    
    class Meta:
        models = User
        fields = ['email', 'username', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number']
        
def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')  
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  
        user.save()
        return user