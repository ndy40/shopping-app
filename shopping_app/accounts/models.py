import dataclasses

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


@dataclasses.dataclass(frozen=True)
class RegisterUserInput:
    first_name: str
    last_name: str
    password: str
    email: str


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
