from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from .models import ShoppingList
from .serializer import ShoppingListSerializer

# Create your views here.


class GetShoppingLists(ListCreateAPIView):
    serializer_class = ShoppingListSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        return ShoppingList.objects.filter(owner=self.request.user)
