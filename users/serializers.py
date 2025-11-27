from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(
        write_only=True,  
        min_length=8,    
        error_messages={'min_length': 'Password must be at least eight characters'} 
    )
    password_confirm = serializers.CharField(write_only=True)  
    
    class Meta:
        model = User  
        fields = ['email', 'username', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number', 'date_of_birth']
        extra_kwargs = {
            'date_of_birth': {'required': True} 
        }
    
    def validate_date_of_birth(self, value):
        """Validate that user is at least 13 years old"""
        today = timezone.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age < 13:
            raise serializers.ValidationError("Users must be at least 13 years old.")
        
        return value
    
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

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'age', 'date_joined']
    
    def get_age(self, obj):
        return obj.age 