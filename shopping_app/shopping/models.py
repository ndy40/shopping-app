from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ShoppingListStatus(models.TextChoices):
    # workflow:
    # - (DRAFT -> [ACTIVE, ARCHIVED, TEMPLATE])
    # - (TEMPLATE -> [DRAFT, ARCHIVED])
    # - (ACTIVE -> [CLOSED, ARCHIVED])
    # TODO: implement workflows
    TEMPLATE = "TEMPLATE", _("Template")
    ARCHIVED = "ARCHIVED", _("Archived")
    DRAFT = "DRAFT", _("Draft")
    ACTIVE = "ACTIVE", _("Active")


class ShoppingItemStatus(models.TextChoices):
    PICKED = "PICKED", _("PICKED")
    UNPICKED = "UNPICKED", _("UNPICKED")


class ShoppingList(models.Model):
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    status = models.CharField(
        max_length=100,
        choices=ShoppingListStatus.choices,
        default=ShoppingListStatus.DRAFT,
        null=True,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def title(self):
        return f"Shopping List {self.created_at.strftime('%Y %B %d')}"


class ShoppingItem(models.Model):
    name = models.CharField(null=False, max_length=255)
    quantity = models.PositiveIntegerField(
        default=1,
        null=True,
    )
    status = models.CharField(
        max_length=100,
        choices=ShoppingItemStatus.choices,
        null=True,
        default=ShoppingItemStatus.UNPICKED,
    )
    shopping_list = models.ForeignKey(
        ShoppingList, on_delete=models.CASCADE, related_name="shopping_list", null=True
    )
