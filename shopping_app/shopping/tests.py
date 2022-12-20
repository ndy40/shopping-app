import json

from django.urls import reverse
from jsonschema import validate
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from shopping import views
from shared import test_utils

# Create your tests here.

SHOPPING_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "quantity": {"type": "integer"},
        "status": {"type": "string", "enum": ["PICKED", "UNPICKED"]},
    },
}

SHOPPING_LIST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "status": {
            "type": "string",
            "enum": [
                "DRAFT",
                "ACTIVE",
                "ARCHIVED",
                "TEMPLATE",
            ],
        },
        "shopping_items": {"type": "array", "items": SHOPPING_ITEM_SCHEMA},
    },
}

ARRAY_OF_SHOPPING_LISTS_SCHEMA = {"type": "array", "items": SHOPPING_LIST_SCHEMA}


class ShoppingListTests(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = test_utils.create_user()
        self.shopping_list = test_utils.create_shopping_list_for_user(
            self.user, ["item1"]
        )

    def test_fetching_shopping_lists_for_user(self):
        # Configure
        request = self.factory.get("/api/shopping_lists/")
        force_authenticate(request, user=self.user)

        # Action
        response = views.GetShoppingCollectionView.as_view()(request)

        # Assert
        assert response.status_code == status.HTTP_200_OK, response.content
        assert (
            validate(instance=response.data, schema=ARRAY_OF_SHOPPING_LISTS_SCHEMA)
            is None
        )

    def test_fetching_shopping_list_item_belonging_to_user(self):
        # Configure
        request = self.factory.get(
            reverse(
                "api:shopping_list:shopping_list_item",
                kwargs={"pk": self.shopping_list.id},
            )
        )
        force_authenticate(request, user=self.user)

        # Action
        response = views.GetShoppingListItemView.as_view()(
            request, pk=self.shopping_list.id
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK, response.content
        assert validate(instance=response.data, schema=SHOPPING_LIST_SCHEMA) is None

    def test_fetching_shopping_list_item_not_belonging_to_user_returns_404(self):
        # Configure
        request = self.factory.get(
            reverse("api:shopping_list:shopping_list_item", kwargs={"pk": 100})
        )
        force_authenticate(request, user=self.user)

        # Action
        response = views.GetShoppingListItemView.as_view()(request, pk=100)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.data

    def test_create_shopping_list_without_shopping_item_for_user_returns_201_created(
        self,
    ):
        # configure
        data = {"status": "DRAFT"}
        requests = self.factory.post(
            reverse("api:shopping_list:shopping_lists_collection"), data
        )
        force_authenticate(requests, user=self.user)

        # Action
        response = views.GetShoppingCollectionView.as_view()(requests)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_shopping_list_with_shopping_item_for_user_returns_200_created(self):
        data = {
            "status": "DRAFT",
            "shopping_items": [
                {
                    "name": "item01",
                }
            ],
        }
        requests = self.factory.post(
            reverse("api:shopping_list:shopping_lists_collection"), data
        )
        force_authenticate(requests, user=self.user)

        # Action
        response = views.GetShoppingCollectionView.as_view()(requests)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_items_to_shopping_lists_using_patch_returns_updated_shopping_list(
        self,
    ):
        data = {
            "status": "DRAFT",
            "shopping_items": [
                {
                    "name": "item01",
                }
            ],
        }
        requests = self.factory.post(
            reverse("api:shopping_list:shopping_lists_collection"), data
        )
        force_authenticate(requests, user=self.user)

        # Action
        response = views.GetShoppingCollectionView.as_view()(requests)

        patch_data = {"shopping_items": [{"name": "item02"}]}
        pk = response.data["id"]
        requests = self.factory.patch(
            reverse("api:shopping_list:shopping_list_item", kwargs={"pk": pk}),
            patch_data,
        )
        force_authenticate(requests, user=self.user)
        patch_resp = views.GetShoppingListItemView.as_view()(requests, pk=pk)
        patch_resp.render()

        assert patch_resp.status_code == status.HTTP_200_OK, patch_resp.content
        assert len(patch_resp.data["shopping_items"]) == 2

    def test_add_items_to_shopping_lists_update_item_and_new_item_in_patch(self):
        data = {
            "status": "DRAFT",
            "shopping_items": [
                {
                    "name": "item01",
                }
            ],
        }
        requests = self.factory.post(
            reverse("api:shopping_list:shopping_lists_collection"), data
        )
        force_authenticate(requests, user=self.user)

        # Action
        response = views.GetShoppingCollectionView.as_view()(requests)

        shopping_item = response.data["shopping_items"][0]

        patch_data = {
            "shopping_items": [
                {"id": shopping_item["id"], "quantity": 2},
                {"name": "item02", "quantity": 4},
            ]
        }
        pk = response.data["id"]
        requests = self.factory.patch(
            reverse("api:shopping_list:shopping_list_item", kwargs={"pk": pk}),
            patch_data,
        )
        force_authenticate(requests, user=self.user)
        patch_resp = views.GetShoppingListItemView.as_view()(requests, pk=pk)
        patch_resp.render()

        assert patch_resp.status_code == status.HTTP_200_OK, patch_resp.content
        assert patch_resp.data["shopping_items"][0]["quantity"] == 2
        assert patch_resp.data["shopping_items"][1]["quantity"] == 4
        assert patch_resp.data["shopping_items"][1]["name"] == "item02"

    # TODO:
    # 3. Add test to delete a single item from shopping list
    # 4. Add test to completely empty shopping list - shopping_list/{id}/empty
