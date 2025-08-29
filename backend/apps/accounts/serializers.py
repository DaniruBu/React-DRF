from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate_email(self, value):
        try:
            EmailValidator()(value)
        except DjangoValidationError:
            raise ValidationError("Invalid email address")
        
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email is already taken")
        
        return BaseUserManager.normalize_email(value)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user