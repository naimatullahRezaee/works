import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.slug = self.scope['url_route']['kwargs']['course_slug']
        # print(self.slug)
        # self.room_group_name = 'chat_%s' % self.slug
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, 
        #     self.channel_name
        # )
        self.accept()

    def disconnect(self, close_code):
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, 
        #     self.channel_name
        # )
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        self.send(text_data=json.dumps({"message" : message}))
        # async_to_sync(self.channel_layer.group.send)(
        #     self.room_group_name, {
        #         'type' : 'chat_messagae', 
        #         'message' : message
        #     }
        # )

    # def chat_message(self, event):
    #     self.send(text_data=json.dumps(event))