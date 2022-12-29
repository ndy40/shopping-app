from django.urls import path

from . import views

app_name = "shopping_app.shopping"

urlpatterns = [
    path(
        "",
        views.ShoppingCollectionView.as_view(),
        name="shopping_lists_collection",
    ),
    path(
        "<int:pk>/empty/",
        views.EmptyShoppingListView.as_view(),
        name="empty_shopping_list",
    ),
    path(
        "<int:pk>/",
        views.ShoppingListItemView.as_view(),
        name="shopping_list_item",
    ),
    path("item/<int:pk>/", views.ShoppingItemView.as_view(), name="shopping_item"),
    path("views/", views.view_page),
]
