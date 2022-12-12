from rest_framework import serializers

from .models import ShoppingList, ShoppingItem


class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = "__all__"


class ShoppingListSerializer(serializers.ModelSerializer):
    shopping_items = ShoppingItemSerializer(many=True, required=False)

    class Meta:
        model = ShoppingList
        fields = ("id", "title", "status", "shopping_items")
