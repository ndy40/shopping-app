from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from shopping.models import ShoppingList


@receiver(post_save, sender=ShoppingList)
def publish_shopping_list_updates(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    channel_grp_name = f"channel_{str(instance.sub_channel)}"
    async_to_sync(channel_layer.group_send)(
        channel_grp_name,
        {"type": "shopping.list.update", "data": str(instance.sub_channel)},
    )
