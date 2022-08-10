from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import File
from project.models import Project
from django.views.decorators.csrf import csrf_exempt


class EditFile(WebsocketConsumer):
    @csrf_exempt
    def connect(self):
        self.room_group_name = 'weEdit'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    @csrf_exempt
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    @csrf_exempt
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        projectID = text_data_json['projectID']
        fileID = text_data_json['fileID']
        if projectID == -1:
            projectID = -1
        else:
            project = Project.objects.get(projectID=projectID)
            project.is_edit = (project.is_edit + 1) % 2
            project.save()
        file = File.objects.get(fileID=fileID)
        file.content = content
        file.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'edit_file',
                'content': content,
                'fileID': fileID,
                'projectID': projectID
            }
        )

    # Receive message from room group
    @csrf_exempt
    def edit_file(self, event):
        content = event['content']
        fileID = event['fileID']
        projectID = event['projectID']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'content': content,
            'fileID': fileID,
            'projectID': projectID
        }))
