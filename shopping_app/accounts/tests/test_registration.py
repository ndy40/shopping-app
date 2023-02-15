from functools import cached_property

from accounts.seed_factories import UserFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def get_access_token_header(self, user):
        payload = {"email": user.email, "password": "fakepassword"}

        resp = self.client.post(reverse("api:accounts:rest_login"), data=payload)
        return {"HTTP_AUTHORIZATION": "Bearer " + resp.json().get("access_token")}

    def test_new_user_registration_succeeds_and_returns_token(self):
        payload = {
            "first_name": "user1",
            "last_name": "user1",
            "email": "user1@mail.com",
            "password": "fakepassword",
        }

        resp = self.client.post(
            reverse("api:accounts:rest_register"), data=payload, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        assert {"access_token", "refresh_token"}.issubset(resp.json())

    def test_duplicate_email_registration_does_not_succeed_with_400_bad_request_response(
        self,
    ):
        UserFactory(email="user1@mail.com")

        payload = {
            "first_name": "user1",
            "last_name": "user1",
            "email": "user1@mail.com",
            "password": "fakepassword",
        }

        resp = self.client.post(
            reverse("api:accounts:rest_register"), data=payload, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_succeeds_with_valid_credentials(self):
        payload = {"email": self.user.email, "password": "fakepassword"}

        resp = self.client.post(reverse("api:accounts:rest_login"), data=payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        assert {"access_token", "refresh_token"}.issubset(resp.json())

    def test_user_login_fails_with_invalid_credentials(self):
        payload = {"email": self.user.email, "password": "invalid_password"}

        resp = self.client.post(reverse("api:accounts:rest_login"), data=payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST, resp.json())

    def test_login_user_can_fetch_profile(self):
        resp = self.client.get(
            reverse("api:accounts:rest_user_details"),
            **self.get_access_token_header(self.user)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.json())
        self.assertEqual(resp.json().get("pk"), self.user.pk)

    def test_user_can_change_their_first_name_with_patch(self):
        resp = self.client.patch(
            reverse("api:accounts:rest_user_details"),
            data={"first_name": "new name"},
            **self.get_access_token_header(self.user)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.json())
        self.assertEqual(resp.json().get("first_name"), "new name", resp.json())

    def test_user_logout_works(self):
        payload = {"email": self.user.email, "password": "fakepassword"}

        resp = self.client.post(reverse("api:accounts:rest_login"), data=payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(reverse("api:accounts:rest_logout"))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
