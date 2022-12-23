import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.urls import path
from shopping.models import ShoppingList
from shopping.serializers import ShoppingListSerializer


class HelloConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test"

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "shopping_evt", "data": data["shopping_list"]}
        )

    def shopping_evt(self, event):
        print("event here")
        shopping_list = ShoppingList.objects.get(pk=event["data"])
        self.send(
            text_data=json.dumps({"data": ShoppingListSerializer(shopping_list).data})
        )


websocket_urlpatterns = [
    path("events/", HelloConsumer.as_asgi()),
]
