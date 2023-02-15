from django.apps import AppConfig
from django.conf import settings


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from .serializers import RegisterSerializer

        settings.REST_AUTH_REGISTER_SERIALIZERS = {
            "REGISTER_SERIALIZER": RegisterSerializer
        }
