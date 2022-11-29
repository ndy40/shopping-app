from dataclasses import asdict

from django.contrib.auth.models import User

from .models import RegisterUserInput

from . import exceptions


def create_user(input_params: RegisterUserInput):
    try:
        User.objects.get(email=input_params.email)
        raise exceptions.UserAlreadyExists("User already exists")
    except User.DoesNotExist:
        params = asdict(input_params)

        if 'password' not in params:
            raise ValueError('Password must be provided.')

        password = params['password']

        del params['password']

        user = User.objects.create(
            **asdict(input_params)
        )

        user.set_password(password)
        user.save()

        return user
