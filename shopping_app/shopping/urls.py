from django.urls import path

from . import views

app_name = "shopping_app.shopping"

urlpatterns = [
    path("", views.GetShoppingLists.as_view(), name="get_shopping_lists"),
]
