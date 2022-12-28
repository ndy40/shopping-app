from .settings import *  # noqa

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025

DISABLE_SIGNALS = False

LOGGING["handlers"]["console"] = {  # noqa: F405
    "level": "DEBUG",
    "filters": ["require_debug_true"],
    "class": "logging.StreamHandler",
}

LOGGING["loggers"]["django.db.backends"] = {  # noqa: F405
    "handlers": ["console"],
    "level": "DEBUG",
}
