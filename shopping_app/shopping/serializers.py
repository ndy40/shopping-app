from rest_framework import serializers

from .models import ShoppingItem, ShoppingList


class ShoppingItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        model = ShoppingItem
        exclude = ("shopping_list",)


class ShoppingListSerializer(serializers.ModelSerializer):
    shopping_items = ShoppingItemSerializer(many=True, required=False)

    sub_channel = serializers.UUIDField(read_only=True)

    class Meta:
        model = ShoppingList
        fields = ["id", "title", "status", "shopping_items", "sub_channel"]

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
        print("val data", validated_data)
        if "shopping_items" in validated_data:
            shopping_items = validated_data.pop(
                "shopping_items", instance.shopping_items
            )

        updated_shopping_list = super().update(instance, validated_data)

        if shopping_items:
            for item in shopping_items:
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
