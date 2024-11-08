import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Use a unique group name based on the user id
        user_id = self.scope['user'].id if self.scope['user'].is_authenticated else 'guest'
        self.group_name = f"notifications_{user_id}"

        # Add the consumer to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the consumer from the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            # Parse the incoming JSON message
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError:
            # Handle JSON errors gracefully
            await self.send(text_data=json.dumps({'error': 'Invalid JSON'}))
            return

        # Print received data for debugging purposes (consider removing this in production)
        print("Received data:", text_data_json)

        # Send acknowledgment back to the client
        await self.send(text_data=json.dumps({'message': 'Hello Client'}))

        # Extract the message part of the data
        message = text_data_json.get('message', 'No message received')

        # Send the message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )

    async def send_notification(self, event):
        # Extract the message from the event
        message = event['message']

        # Log the outgoing message for debugging
        print("Sending message:", message)

        # Send the message to the WebSocket client
        await self.send(text_data=json.dumps({
            'message': message
        }))
