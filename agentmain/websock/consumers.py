from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer
from channels.consumer import SyncConsumer, AsyncConsumer
import json
from asgiref.sync import async_to_sync
import asyncio
from channels.exceptions import StopConsumer
import urllib.parse as parser


class EchoChat(WebsocketConsumer):
    # /////////////////syncron///////////////
    def connect(self):
        self.echo_room = 'echo_rooom'
        # self.user = self.scope['user']
        # self.scope['session']['uname'] = 'purya'
        # self.scope['session']['pname'] = 'bzp'
        # self.scope['session'].save()
        # print(self.scope['session'].get('pname'))
        query = self.scope['query_string']
        decode = parser.parse_qs(query.decode('utf-8'))
        print(decode)


        async_to_sync(self.channel_layer.group_add)(
                self.echo_room,
                self.channel_name
            )

        self.accept()  

    def disconnect(self, code):
       async_to_sync(self.channel_layer.group_discard)(
            self.echo_room,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):

        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            self.send(text_data=json.dumps({'message': message + '/ sent from sever'}))
        elif bytes_data:
            self.send(bytes_data=bytes_data)
    def echo_message(self, event):
        # print(event)
        # bibil = json.dumps(event)
        # print(bibil)
        self.send(text_data=json.dumps(event))     

    # ///////////asyncron////////////////////////
    # async def websocket_connect(self, message):
    #     await self.send({
    #         'type': 'websocket.accept'
    #     })

    # async def websocket_receive(self, event):
    #     await self.send({
    #         "type": "websocket.send",
    #         "text": event["text"],
    #     })


# write with generic consumers:

# class ChatConsumer(AsyncWebsocketConsumer):

# /////////////////syncron///////////////
# def connect(self):
#     # print(self.channel_name)
#     self.username = self.scope['url_route']['kwargs']['username']
#     self.group_name = f'chat_{self.username}'
#     # print(self.group_name)
#     self.channel_layer.group_add(
#         self.group_name,
#         self.username
#     )
#     self.accept()
#
# def disconnect(self, code):
#     pass
#
# def receive(self, text_data=None, bytes_data=None):
#     if text_data:
#         text_data_json = json.loads(text_data)

# ///////////asyncron////////////////////////
# async def connect(self):
#     self.user_id = self.scope['url_route']['kwargs']['username']
#     self.group_name = f"chat_{self.user_id}"
#
#     await self.channel_layer.group_add(
#         self.group_name,
#         self.channel_name
#     )
#
#     await self.accept()
#
# async def disconnect(self, close_code):
#     await self.channel_layer.group_discard(
#         self.group_name,
#         self.channel_name
#     )
#
# async def receive(self, text_data=None, bytes_data=None):
#     if text_data:
#         text_data_json = json.loads(text_data)
#         username = text_data_json['receiver']
#         user_group_name = f"chat_{username}"
#
#         await self.channel_layer.group_send(
#             user_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': text_data
#             }
#         )
#
# async def chat_message(self, event):
#     message = event['message']
#
#     await self.send(text_data=message)

# write with basic consumers
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user_id = self.scope['url_route']['kwargs']['username']
        self.group_name = f"chat_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()

    async def websocket_receive(self, event):
        # print(self.scope['method'])
        # print(self.scope['headers'])
        # print(self.scope['path'])
        # print(self.scope['user'])

        # print(event)
        text_data = event.get('text', None)
        # print(text_data)
        if text_data:
            text_data_json = json.loads(text_data)
            username = text_data_json['receiver']
            user_group_name = f"chat_{username}"

            await self.channel_layer.group_send(
                user_group_name,
                {
                    'type': 'chat_message',
                    'message': text_data
                }
            )

            await self.channel_layer.group_send(
                'echo_rooom',
                {
                    'type': 'echo_message',
                    'message': text_data
                }
            )


    async def chat_message(self, event):
        message = event['message']

        await self.send({
            'type':'websocket.send',
            'text':message
        })
















# from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
# from channels.consumer import SyncConsumer, AsyncConsumer
# from channels.exceptions import StopConsumer
# from asgiref.sync import async_to_sync
# import json

# class EchoChat(WebsocketConsumer):
#     def connect(self):
#         self.room_id = "echo_1"

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_id,
#             self.channel_name
#         )
        
#         self.accept()
        
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_id,
#             self.channel_name
#         )

#     def receive(self, text_data=None, bytes_data=None):
#         if text_data:
#             self.send(text_data=text_data + " - Sent By Server")
#         elif bytes_data:
#             self.send(bytes_data=bytes_data)

#     def echo_message(self, event):
#         message = event['message']

#         self.send(text_data=message)


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user_id = self.scope['url_route']['kwargs']['username']
#         self.group_name = f"chat_{self.user_id}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()
    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data=None, bytes_data=None):
#         if text_data:
#             text_data_json = json.loads(text_data)
#             username = text_data_json['receiver']
#             user_group_name = f"chat_{username}"
            
#             await self.channel_layer.group_send(
#                 user_group_name,
#                 {
#                     'type': 'chat_message',
#                     'message': text_data
#                 }
#             )

#     async def chat_message(self, event):
#         message = event['message']

#         await self.send(text_data=message)


# class ChatConsumer2(AsyncConsumer):
#     async def websocket_connect(self, event):
#         self.user_id = self.scope['url_route']['kwargs']['username']
#         self.group_name = f"chat_{self.user_id}"

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.send({
#             'type': 'websocket.accept'
#         })

#     async def websocket_disconnect(self, event):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )
#         raise StopConsumer()


#     async def websocket_receive(self, event):
#         text_data = event.get('text', None)
#         bytes_data = event.get('bytes', None)

#         if text_data:
#             text_data_json = json.loads(text_data)
#             username = text_data_json['receiver']
#             user_group_name = f"chat_{username}"
            
#             await self.channel_layer.group_send(
#                 user_group_name,
#                 {
#                     'type': 'chat_message',
#                     'message': text_data
#                 }
#             )
#             await self.channel_layer.group_send(
#                 'echo_1',
#                 {
#                     'type': 'echo_message',
#                     'message': text_data
#                 }
#             )

#     async def chat_message(self, event):
#         message = event['message']

#         await self.send({
#             'type': 'websocket.send',
#             'text': message
#         })



# class TestConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
    
#         await self.accept()
    
#     async def disconnect(self, close_code):
#         pass

#     async def receive_json(self, content):
#         await self.send_json(content)
class Test(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope['user']
        print(f'salam {self.user}')
    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        self.send(text_data=f'received {text_data} from {self.user}')
     