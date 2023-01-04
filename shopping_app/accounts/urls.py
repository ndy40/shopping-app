from allauth.account.views import ConfirmEmailView
from django.urls import include, path, re_path

app_name = "accounts"

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
