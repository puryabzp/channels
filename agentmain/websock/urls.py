from django.urls import path

from .views import index, room, image_echo, join_chat,httptows,cookies

urlpatterns = [
    path('', index, name='index'),
    path('rooms/<str:room_name>/', room, name='room'),
    path('image/', image_echo, name='echo_image'),
    path('twoway-chat/<str:user_name>/', join_chat, name='join_chat'),
    path('http-to-ws/<str:user_name>/', httptows, name='httptows'),
    path('test_cookie/', cookies, name='test_cookie'),
]
