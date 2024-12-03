import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


# create consumer for update price web socket
class PriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "price_consumer"
        self.channel_layer = get_channel_layer()
        if not self.channel_layer:
            await self.close()
            return
        # Add this connection to the group

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        await self.send(
            text_data=json.dumps({"message": "Welcome to the Price WebSocket!"})
        )

    async def disconnect(self, close_code):

        self.channel_layer = get_channel_layer()
        if not self.channel_layer:
            await self.close()
            return
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        self.channel_layer = get_channel_layer()
        if not self.channel_layer:
            await self.close()
            return

        await self.channel_layer.group_send(
            self.group_name, {"type": "chat_message", "message": message}
        )

        # Echo the message back to the client
        await self.send(text_data=json.dumps({"message": message}))

    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
