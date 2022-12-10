from django.urls import path, include

app_name = "shopping_app.api"

urlpatterns = [
    path("accounts/", include("accounts.urls", namespace="api")),
]
