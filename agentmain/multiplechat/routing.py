from django.urls import path

from .consumers import ChatConsumer,VideoChatConsumer

websocket_urlpatterns = [
    path('ws/multiplechat/<str:chat_id>/', ChatConsumer.as_asgi()),
    path('ws/videochat/', VideoChatConsumer.as_asgi())
]
