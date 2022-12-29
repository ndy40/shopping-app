from accounts.seed_factories import UserFactory
from django.urls import reverse
from jsonschema import validate
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from shared import test_utils
from shopping import views
from shopping.seed_factories import SharedWithFactory, ShoppingListFactory

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

SHOPPING_LIST_ITEM_ROUTE = "api:shopping_list:shopping_list_item"
SHOPPING_LIST_COLLECTION_ROUTE = "api:shopping_list:shopping_lists_collection"
SHOPPING_LIST_ITEM_EMPTY = "api:shopping_list:empty_shopping_list"


class ShoppingListTests(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = test_utils.create_user()
        self.shopping_list = test_utils.create_shopping_list_for_user(
            self.user, ["item1"]
        )

    def test_fetching_shopping_lists_for_user(self):
        # Configure
        request = self.factory.get(reverse(SHOPPING_LIST_COLLECTION_ROUTE))
        force_authenticate(request, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(request)

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
                SHOPPING_LIST_ITEM_ROUTE,
                kwargs={"pk": self.shopping_list.id},
            )
        )
        force_authenticate(request, user=self.user)

        # Action
        response = views.ShoppingListItemView.as_view()(
            request, pk=self.shopping_list.id
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK, response.content
        assert validate(instance=response.data, schema=SHOPPING_LIST_SCHEMA) is None

    def test_fetching_shopping_list_item_not_belonging_to_user_returns_404(self):
        # Configure
        request = self.factory.get(
            reverse(SHOPPING_LIST_ITEM_ROUTE, kwargs={"pk": 100})
        )
        force_authenticate(request, user=self.user)

        # Action
        response = views.ShoppingListItemView.as_view()(request, pk=100)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.data

    def test_create_shopping_list_without_shopping_item_for_user_returns_201_created(
        self,
    ):
        # configure
        data = {"status": "DRAFT"}
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)

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
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)

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
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)

        patch_data = {"shopping_items": [{"name": "item02"}]}
        pk = response.data["id"]
        requests = self.factory.patch(
            reverse(SHOPPING_LIST_ITEM_ROUTE, kwargs={"pk": pk}),
            patch_data,
        )
        force_authenticate(requests, user=self.user)
        patch_resp = views.ShoppingListItemView.as_view()(requests, pk=pk)
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
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)

        shopping_item = response.data["shopping_items"][0]

        patch_data = {
            "shopping_items": [
                {"id": shopping_item["id"], "quantity": 2},
                {"name": "item02", "quantity": 4},
            ]
        }
        pk = response.data["id"]
        requests = self.factory.patch(
            reverse(SHOPPING_LIST_ITEM_ROUTE, kwargs={"pk": pk}),
            patch_data,
        )
        force_authenticate(requests, user=self.user)
        patch_resp = views.ShoppingListItemView.as_view()(requests, pk=pk)
        patch_resp.render()

        assert patch_resp.status_code == status.HTTP_200_OK, patch_resp.content
        assert patch_resp.data["shopping_items"][0]["quantity"] == 2, patch_resp.content
        assert patch_resp.data["shopping_items"][1]["quantity"] == 4, patch_resp.content
        assert (
            patch_resp.data["shopping_items"][1]["name"] == "item02"
        ), patch_resp.content

    def test_delete_shopping_item_from_shopping_list(self):
        data = {
            "status": "DRAFT",
            "shopping_items": [
                {
                    "name": "item01",
                },
                {"name": "item02"},
                {"name": "item03"},
            ],
        }
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)
        shopping_list_id = response.data["id"]
        item_id = response.data["shopping_items"][0]["id"]
        first_item_url = reverse(
            "shopping_app.api:shopping_app.shopping:shopping_item",
            kwargs={"pk": item_id},
        )

        request = self.factory.delete(first_item_url)
        force_authenticate(request, user=self.user)
        response = views.ShoppingItemView.as_view()(request, pk=item_id)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.data

        request = self.factory.get(
            reverse(
                "shopping_app.api:shopping_list:shopping_list_item",
                kwargs={"pk": shopping_list_id},
            )
        )
        force_authenticate(request, user=self.user)
        response = views.ShoppingListItemView.as_view()(request, pk=shopping_list_id)

        assert len(response.data["shopping_items"]) == 2

    def test_empty_shopping_list_succeeds(self):
        data = {
            "status": "DRAFT",
            "shopping_items": [
                {
                    "name": "item01",
                },
                {"name": "item02"},
                {"name": "item03"},
            ],
        }
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)
        shopping_list_id = response.data["id"]

        requests = self.factory.delete(
            reverse(
                "shopping_app.api:shopping_app.shopping:empty_shopping_list",
                kwargs={"pk": shopping_list_id},
            )
        )
        force_authenticate(requests, user=self.user)
        resp = views.EmptyShoppingListView.as_view()(requests, pk=shopping_list_id)

        assert resp.status_code == status.HTTP_204_NO_CONTENT, resp.data

    def test_when_duplicate_shopping_item_is_added_then_post_returns_400_bad_request_response(
        self,
    ):
        data = {
            "status": "DRAFT",
            "shopping_items": [
                {
                    "name": "item01",
                },
                {"name": "item01"},
            ],
        }
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)
        response.render()

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content

    def test_when_duplicate_shopping_item_is_added_then_patch_returns_400_bad_request_response(
        self,
    ):
        data = {
            "status": "DRAFT",
            "shopping_items": [
                {
                    "name": "item01",
                },
                {"name": "item02"},
            ],
        }
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)
        pk = response.data["id"]

        patch_data = {"shopping_items": [{"name": "item02"}]}

        requests = self.factory.patch(
            reverse(SHOPPING_LIST_ITEM_ROUTE, kwargs={"pk": pk}),
            patch_data,
        )
        force_authenticate(requests, user=self.user)
        patch_resp = views.ShoppingListItemView.as_view()(requests, pk=pk)
        patch_resp.render()

        assert patch_resp.status_code == status.HTTP_400_BAD_REQUEST, (
            patch_resp.status_code,
            patch_resp.content,
        )

    def test_when_shopping_item_is_renamed_to_an_existing_items_name_patch_returns_400_bad_request_response(
        self,
    ):
        data = {
            "status": "DRAFT",
            "shopping_items": [
                {
                    "name": "item01",
                },
                {"name": "item02"},
            ],
        }
        requests = self.factory.post(reverse(SHOPPING_LIST_COLLECTION_ROUTE), data)
        force_authenticate(requests, user=self.user)

        # Action
        response = views.ShoppingCollectionView.as_view()(requests)
        pk = response.data["id"]
        first_item = response.data["shopping_items"][0]

        patch_data = {"shopping_items": [{"id": first_item["id"], "name": "item02"}]}

        requests = self.factory.patch(
            reverse(SHOPPING_LIST_ITEM_ROUTE, kwargs={"pk": pk}),
            patch_data,
        )
        force_authenticate(requests, user=self.user)
        patch_resp = views.ShoppingListItemView.as_view()(requests, pk=pk)
        patch_resp.render()

        assert patch_resp.status_code == status.HTTP_400_BAD_REQUEST, (
            patch_resp.status_code,
            patch_resp.content,
        )


class ShoppingListCollaborationTests(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        # create users
        self.user1 = UserFactory()  # user with a shopping list
        self.user2 = UserFactory()  # user that collabs on list belonging to user1
        self.user3 = UserFactory()  # user that doesn't have a list shared with them.

        # Create shopping list
        self.shopping_list = ShoppingListFactory(owner=self.user1)
        SharedWithFactory(shopping_list=self.shopping_list, shared_with=self.user2)

    def test_fetch_shopping_list_user2_is_a_collaborator_on_returns_successful(self):
        request = self.factory.get(SHOPPING_LIST_COLLECTION_ROUTE)
        force_authenticate(request, self.user2)

        resp = views.ShoppingCollectionView.as_view()(request)

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data) == 1

    def test_empty_shopping_list_returned_for_user3(self):
        request = self.factory.get(reverse(SHOPPING_LIST_COLLECTION_ROUTE))
        force_authenticate(request, self.user3)

        resp = views.ShoppingCollectionView.as_view()(request)

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data) == 0

    def test_single_shopping_list_returned_for_user1_who_is_owner(self):
        request = self.factory.get(reverse(SHOPPING_LIST_COLLECTION_ROUTE))
        force_authenticate(request, self.user1)

        resp = views.ShoppingCollectionView.as_view()(request)

        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.data) == 1

    def test_user_cannot_fetch_shopping_list_they_do_not_own_or_share(self):
        request = self.factory.get(reverse(SHOPPING_LIST_COLLECTION_ROUTE))
        force_authenticate(request, self.user1)

        resp = views.ShoppingCollectionView.as_view()(request)
        shopping_list_id = resp.data[0]["id"]

        request = self.factory.get(
            reverse(SHOPPING_LIST_ITEM_ROUTE, kwargs={"pk": shopping_list_id})
        )
        force_authenticate(request, self.user3)

        resp = views.ShoppingListItemView.as_view()(request, pk=shopping_list_id)

        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_when_user_who_is_collaborator_can_add_item_to_shopping_list(self):
        request = self.factory.patch(
            reverse(SHOPPING_LIST_ITEM_ROUTE, kwargs={"pk": self.shopping_list.id}),
            data={"shopping_items": [{"name": "user2-item"}]},
        )
        force_authenticate(request, self.user2)

        resp = views.ShoppingListItemView.as_view()(request, pk=self.shopping_list.id)
        resp.render()

        assert resp.status_code == status.HTTP_200_OK, (
            resp.status_code,
            resp.content,
        )

    def test_when_user_who_is_not_collaborator_can_not_add_item_to_shopping_list(self):
        request = self.factory.patch(
            reverse(SHOPPING_LIST_ITEM_ROUTE, kwargs={"pk": self.shopping_list.id}),
            data={"shopping_items": [{"name": "user2-item"}]},
        )
        force_authenticate(request, self.user3)

        resp = views.ShoppingListItemView.as_view()(request, pk=self.shopping_list.id)
        resp.render()

        assert resp.status_code == status.HTTP_404_NOT_FOUND, (
            resp.status_code,
            resp.content,
        )

    def test_when_user_who_is_not_collaborator_can_not_empty_the_shopping_list(self):

        request = self.factory.delete(
            reverse(SHOPPING_LIST_ITEM_EMPTY, kwargs={"pk": self.shopping_list.id})
        )
        force_authenticate(request, self.user3)

        resp = views.EmptyShoppingListView.as_view()(request, pk=self.shopping_list.id)
        resp.render()

        assert resp.status_code == status.HTTP_404_NOT_FOUND, (
            resp.status_code,
            resp.content,
        )

    def test_when_user_who_is_a_collaborator_can_not_empty_the_shopping_list(self):

        request = self.factory.delete(
            reverse(SHOPPING_LIST_ITEM_EMPTY, kwargs={"pk": self.shopping_list.id})
        )
        force_authenticate(request, self.user2)

        resp = views.EmptyShoppingListView.as_view()(request, pk=self.shopping_list.id)
        resp.render()

        assert resp.status_code == status.HTTP_404_NOT_FOUND, (
            resp.status_code,
            resp.content,
        )

    def test_when_user_who_is_not_owner_of_shopping_list_attempts_to_delete_shopping_list_gets_rejected(
        self,
    ):
        requests = self.factory.delete(
            reverse(SHOPPING_LIST_ITEM_EMPTY, kwargs={"pk": self.shopping_list.id})
        )
        force_authenticate(requests, self.user3)

        resp = views.ShoppingListItemView.as_view()(requests, pk=self.shopping_list.id)
        resp.render()

        assert resp.status_code == status.HTTP_404_NOT_FOUND, (
            resp.status_code,
            resp.content,
        )

    def test_when_user_who_is_a_collaborator_of_shopping_list_attempts_to_delete_shopping_list_gets_rejected(
        self,
    ):
        requests = self.factory.delete(
            reverse(SHOPPING_LIST_ITEM_EMPTY, kwargs={"pk": self.shopping_list.id})
        )
        force_authenticate(requests, self.user2)

        resp = views.ShoppingListItemView.as_view()(requests, pk=self.shopping_list.id)
        resp.render()

        assert resp.status_code == status.HTTP_404_NOT_FOUND, (
            resp.status_code,
            resp.content,
        )
