from dataclasses import asdict

from django.contrib.auth.models import User, Permission

from .models import RegisterUserInput

from . import exceptions


def get_user_shopping_permisisons():
    DEFAULT_SHOPPING_PERMISSIONS = [
        "add_shoppinglist",
        "view_shoppinglist",
        "change_shoppinglist",
        "delete_shoppinglist",
    ]

    return Permission.objects.filter(codename__in=DEFAULT_SHOPPING_PERMISSIONS)


def create_user(input_params: RegisterUserInput):
    try:
        User.objects.get(email=input_params.email)
        raise exceptions.UserAlreadyExists("User already exists")
    except User.DoesNotExist:
        params = asdict(input_params)

        if "password" not in params:
            raise ValueError("Password must be provided.")

        password = params["password"]

        del params["password"]
        User.objects.create_user()
        user = User.objects.create(**asdict(input_params))

        user.set_password(password)
        user.save()

        return user
