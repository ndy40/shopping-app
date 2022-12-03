from rest_framework.generics import ListCreateAPIView

from .serializer import ShoppingListSerializer

# Create your views here.


class GetShoppingLists(ListCreateAPIView):
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        return super().get_queryset()
