import asyncio
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.urls import path
from shopping.models import ShoppingList
from shopping.serializers import ShoppingListSerializer


class ShoppingListConsumer(WebsocketConsumer):
    list_name = None

    def connect(self):
        try:
            shopping_list = self._get_shopping_list(self._get_shopping_channel())
            self.list_name = f"channel_{shopping_list.sub_channel}"

            async_to_sync(self.channel_layer.group_add)(
                self.list_name, self.channel_name
            )
            self.accept()
        except ShoppingList.DoesNotExist:
            self.close()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.list_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(
            self.list_name,
            {"type": "shopping.list.update", "data": self._get_shopping_channel()},
        )

    def shopping_list_update(self, event):
        print("sending update....")
        shopping_list = ShoppingList.objects.get(sub_channel=event["data"])
        self.send(
            text_data=json.dumps({"data": ShoppingListSerializer(shopping_list).data})
        )

    def _get_shopping_channel(self):
        return self.scope["url_route"]["kwargs"].get("sub_channel")

    def _get_shopping_list(self, sub_channel):
        return ShoppingList.objects.get(sub_channel=sub_channel)


websocket_urlpatterns = [
    path("ws/shopping_list/<str:sub_channel>/", ShoppingListConsumer.as_asgi()),
]
