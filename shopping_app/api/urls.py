from django.urls import path, include

app_name = "shopping_app.api"

urlpatterns = [
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("shopping_lists/", include("shopping.urls", namespace="shopping_list")),
]
