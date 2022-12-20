from typing import List, AnyStr

from accounts.seed_factories import UserFactory
from shopping.seed_factories import ShoppingListFactory, ShoppingItemFactory


def create_user():
    return UserFactory(email="user1@email.com")


def create_shopping_list_for_user(user, items=None):
    if items is None:
        items = ["item1"]

    shopping_list = ShoppingListFactory(owner=user)

    for item in items:
        ShoppingItemFactory(shopping_list=shopping_list, name=item)

    shopping_list.refresh_from_db()

    return shopping_list
