import dataclasses

from django.db import models

# Create your models here.


@dataclasses.dataclass(frozen=True)
class RegisterUserInput:
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
