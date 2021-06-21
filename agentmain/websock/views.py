import json
from django.dispatch.dispatcher import receiver

from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from channels.routing import ProtocolTypeRouter
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def index(request):
    return render(request, 'websock/index.html')


def room(request, room_name):
    return render(request, 'websock/room.html', {'room_name': room_name})


def image_echo(request):
    return render(request, 'websock/echo_image.html')


def join_chat(request, user_name):
    print(json.dumps(user_name))
    return render(request, 'websock/join_chat.html', {'username_json': mark_safe(json.dumps(user_name))})

def httptows(request,user_name):
    receiver = request.GET['receiver']
    text = request.GET['text']
    group_name = f"chat_{receiver}"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type' : 'chat_message',
            'message': json.dumps({'sender':user_name,'receiver':receiver,'text':text})
        }
    )
    return HttpResponse('DONE!')


    # receiver = request.GET['receiver']
    # text = request.GET['text']
    # channel_layer = get_channel_layer()
    # group_name = f"chat_{receiver}"

    # async_to_sync(channel_layer.group_send)(
    #     group_name,
    #     {
    #         'type': 'chat_message',
    #         'message': json.dumps({'sender': user_name, 'receiver': receiver, 'text': text})
    #     }
    # )

    # return HttpResponse('Message Sent')

def cookies(request):
    if not request.COOKIES.get('sharid'):
        response = HttpResponse("Visiting for the first time.")
        response.set_cookie('sharid', 'shemila')
        return response
    else:
        return HttpResponse("Your favorite team is {}".format(request.COOKIES['sharid']))
    # print(request.COOKIES)
    # return HttpResponse('hi')