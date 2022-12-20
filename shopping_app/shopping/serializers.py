from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import ShoppingList, ShoppingItem


class ShoppingItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    resource_link = serializers.URLField(required=False, read_only=True)

    class Meta:
        model = ShoppingItem
        exclude = ("shopping_list",)


class ShoppingListSerializer(serializers.ModelSerializer):
    shopping_items = ShoppingItemSerializer(many=True, required=False)

    class Meta:
        model = ShoppingList
        fields = [
            "id",
            "title",
            "status",
            "shopping_items",
        ]

    def create(self, validated_data):
        shopping_items = None

        if "shopping_items" in validated_data:
            shopping_items = validated_data.pop("shopping_items")

        shopping_list = super().create(validated_data)

        if shopping_items:
            for item in shopping_items:
                ShoppingItem.objects.create(shopping_list=shopping_list, **item)

        shopping_list.refresh_from_db()
        return shopping_list

    def update(self, instance, validated_data):
        shopping_items = None

        if "shopping_items" in validated_data:
            shopping_items = validated_data.pop("shopping_items")

        updated_shopping_list = super().update(instance, validated_data)

        if shopping_items:
            for item in shopping_items:
                if "id" in item:
                    item_id = item.pop("id")
                    ShoppingItem.objects.filter(pk=item_id).update(**item)
                else:
                    ShoppingItem.objects.create(
                        **item, shopping_list=updated_shopping_list
                    )

        updated_shopping_list.refresh_from_db()
        return updated_shopping_list
