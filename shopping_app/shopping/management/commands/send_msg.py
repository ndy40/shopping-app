from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management import BaseCommand
from django_eventstream import send_event


class Command(BaseCommand):
    def handle(self, *args, **options):
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "tests", {"type": "shopping_evt", "data": 17}
        )
