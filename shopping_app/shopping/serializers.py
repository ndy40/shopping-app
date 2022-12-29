from accounts.models import User
from rest_framework import serializers

from .models import ShoppingItem, ShoppingList


class ShoppingItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = ShoppingItem
        exclude = ("shopping_list",)


class SharedWithSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(source="get_full_name")

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "first_name",
            "last_name",
        ]


class ShoppingListSerializer(serializers.ModelSerializer):
    shopping_items = ShoppingItemSerializer(many=True, required=False)
    sub_channel = serializers.UUIDField(read_only=True)
    shared_with = SharedWithSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = ShoppingList
        fields = [
            "id",
            "title",
            "status",
            "shopping_items",
            "sub_channel",
            "shared_with",
            "owner_id",
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
            shopping_items = validated_data.pop(
                "shopping_items", instance.shopping_items
            )

        updated_shopping_list = super().update(instance, validated_data)

        if shopping_items:
            for item in shopping_items:
                if "name" in item:
                    self._validate_duplicate_shopping_items(instance.id, item)

                if "id" in item:
                    item_id = item.pop("id")
                    ShoppingItem.objects.filter(pk=item_id).update(**item)
                else:
                    if ShoppingItem.objects.filter(
                        name=item["name"], shopping_list=instance.id
                    ).exists():
                        raise serializers.ValidationError(
                            f"Duplicate shopping item \"{item['name']}\" found"
                        )

                    ShoppingItem.objects.create(
                        **item, shopping_list=updated_shopping_list
                    )

        updated_shopping_list.refresh_from_db()
        return updated_shopping_list

    def _validate_duplicate_shopping_items(self, instance_id: int, item: dict):
        if ShoppingItem.objects.filter(
            shopping_list_id=instance_id, name=item["name"]
        ).exists():
            raise serializers.ValidationError(f'Item already exists {item["name"]}')

        return True

    def validate_shopping_items(self, value):
        found = set()
        for item in value:
            line_item = dict(item)
            if "name" in line_item:
                if line_item["name"] in found:
                    raise serializers.ValidationError(
                        f"Duplicate shopping items {line_item['name']}"
                    )

                found.add(line_item["name"])

        return value
