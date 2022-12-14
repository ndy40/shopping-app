import logging

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators
from .models import RegisterUserInput, User
from .services import create_user


_logger = logging.getLogger(__package__)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        data = RegisterUserInput(**validated_data)
        user = create_user(data)
        _logger.info(f"Created new user {validated_data['email']}")
        return user
