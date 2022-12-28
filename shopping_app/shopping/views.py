from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.generics import (
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import ShoppingItem, ShoppingList
from .serializers import ShoppingItemSerializer, ShoppingListSerializer

# Create your views here.


class GetShoppingCollectionView(ListCreateAPIView):
    serializer_class = ShoppingListSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        return ShoppingList.objects.filter(owner=self.request.user)

    def perform_create(self, serializer: Serializer):
        serializer.validated_data["owner"] = self.request.user
        return super().perform_create(serializer)


class GetShoppingListItemView(RetrieveUpdateAPIView, DestroyAPIView):
    serializer_class = ShoppingListSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        return ShoppingList.objects.filter(owner=self.request.user).prefetch_related(
            "shopping_items"
        )


class EmptyShoppingListView(DestroyAPIView):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        return ShoppingList.objects.filter(owner=self.request.user)

    def delete(self, request, pk: int):
        shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
        ShoppingItem.objects.filter(shopping_list=shopping_list).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingItemView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer


def view_page(request):
    return render(request, "shopping/index.html", {})
