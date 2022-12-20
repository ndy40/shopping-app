from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .services import get_user_shopping_permisisons


@receiver(pre_save, model=User)
def add_default_user_permissions(_, instance: User, **kwargs):
    instance.user_permissions_set.add(get_user_shopping_permisisons())
    instance.save()


# TODO:
# 1. Add User created signal for sending email.
# 2. Add signal for password reset email.
# 3. Add password resend email signal
