from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import File


class EditFile(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'weEdit'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        fileID = text_data_json['fileID']
        file = File.objects.get(fileID=fileID)
        file.content = content
        file.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'edit_file',
                'content': content,
                'fileID': fileID
            }
        )

    # Receive message from room group
    def edit_file(self, event):
        content = event['content']
        fileID = event['fileID']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'content': content,
            'fileID': fileID
        }))
