from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Page, Prototype
from django.views.decorators.csrf import csrf_exempt


class Editprototype(WebsocketConsumer):
    @csrf_exempt
    def connect(self):
        # print(pageID)
        self.room_group_name = 'we_Edit'

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
        prototypeID = text_data_json['prototypeID']
        prototype = Prototype.objects.get(prototypeID=prototypeID)
        pageID = text_data_json['pageID']
        pageComponentData = text_data_json['pageComponentData']
        pageCanvasStyle = text_data_json['pageCanvasStyle']
        page = Page.objects.get(pageID=pageID, prototype=prototype)
        page.pageComponentData = pageComponentData
        page.pageCanvasStyle = pageCanvasStyle
        page.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'edit_prototype',
                'prototypeID': prototypeID,
                'pageID': pageID,
                'pageComponentData': pageComponentData,
                'pageCanvasStyle': pageCanvasStyle
            }
        )

    # Receive message from room group
    @csrf_exempt
    def edit_prototype(self, event):
        prototypeID = event['prototypeID']
        pageID = event['pageID']
        pageComponentData = event['pageComponentData']
        pageCanvasStyle = event['pageCanvasStyle']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'prototypeID': prototypeID,
            'pageID': pageID,
            'pageComponentData': pageComponentData,
            'pageCanvasStyle': pageCanvasStyle
        }))
