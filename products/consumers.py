# product/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProductNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "product_notifications"
        # Ajouter ce client à un groupe de notifications
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Retirer ce client du groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Envoyer la notification au groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'product_notification',
                'message': data['message']
            }
        )

    async def product_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
