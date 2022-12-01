from django.urls import path

from accounts.views import RegisterUserView


app_name = "accounts"

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register_user"),
]
