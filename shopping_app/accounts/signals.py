from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .services import get_user_shopping_permisisons


@receiver(pre_save, model=User)
def add_default_user_permissions(_, instance: User, **kwargs):
    instance.user_permissions_set.add(get_user_shopping_permisisons())
    instance.save()
