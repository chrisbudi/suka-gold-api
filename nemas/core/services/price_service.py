import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class price_service:
    def publish_price(self, data):
        channel_layer = get_channel_layer()
        self.group_name = "price_consumer"
        if not channel_layer:
            return

        print("Publishing price to websocket consumer")
        async_to_sync(channel_layer.group_send)(
            "price_consumer", {"type": "chat_message", "message": data}
        )
        pass
