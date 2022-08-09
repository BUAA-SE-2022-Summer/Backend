from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Page, Prototype, PageUse
from django.views.decorators.csrf import csrf_exempt


def get_page_use_list(page):
    user_list = []
    page_use_list = PageUse.objects.filter(page=page)
    for i in page_use_list:
        user_list.append({'userID': i.user.userID, 'userName': i.user.userName, 'img': i.user.img})
    return user_list


class Editprototype(WebsocketConsumer):
    @csrf_exempt
    def connect(self):
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
        user_list = get_page_use_list(page)
        if page.pageComponentData == pageComponentData and page.pageCanvasStyle == pageCanvasStyle:
            result = False
        else:
            page.pageComponentData = pageComponentData
            page.pageCanvasStyle = pageCanvasStyle
            page.save()
            result = True
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'edit_prototype',
                'prototypeID': prototypeID,
                'pageID': pageID,
                'pageComponentData': pageComponentData,
                'pageCanvasStyle': pageCanvasStyle,
                'result': result,
                'user_list': user_list
            }
        )

    # Receive message from room group
    @csrf_exempt
    def edit_prototype(self, event):
        prototypeID = event['prototypeID']
        pageID = event['pageID']
        pageComponentData = event['pageComponentData']
        pageCanvasStyle = event['pageCanvasStyle']
        result = event['result']
        user_list = event['user_list']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'prototypeID': prototypeID,
            'pageID': pageID,
            'pageComponentData': pageComponentData,
            'pageCanvasStyle': pageCanvasStyle,
            'result': result,
            'user_list': user_list,
        }))
