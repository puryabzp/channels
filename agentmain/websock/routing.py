from django.urls import re_path, path
from .consumers import EchoChat,ChatConsumer,Test

websocket_urlpatterns = [
    re_path(r'ws/chat/rooms/(?P<room_name>\w+)/$', EchoChat.as_asgi()),
    path('ws/chat/images/', EchoChat.as_asgi()),
    path('ws/chat/twoway-chat/<str:username>/', ChatConsumer.as_asgi()),
    path('ws/test/test/',Test.as_asgi() )
]
