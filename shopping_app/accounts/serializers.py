import logging

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "password": self.validated_data.get("password", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)

        self.cleaned_data = self.get_cleaned_data()

        user = adapter.save_user(request, user, self, commit=False)
        if "password" in self.cleaned_data:
            try:
                user.password = make_password(
                    adapter.clean_password(self.cleaned_data["password"], user=user)
                )
            except ValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
