# serializers.py
from rest_framework import serializers
from .models import User
from .validators import validate_password, phone_validator
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(required=True, validators=[phone_validator])

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'name', 'age', 'gender', 'address', 'phone', 'is_email_verified')

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
