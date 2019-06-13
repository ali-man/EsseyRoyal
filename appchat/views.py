import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from appchat.models import Chat
from appusers.models import User


def main_chat(request):
    messages_from_chat = Chat.objects.all()[:10]
    context = {
        'messages_from_chat': messages_from_chat,
    }
    return render(request, 'chat/main.html', context=context)


def chat_ajax(request):
    messages_from_chat = Chat.objects.all()[:10]
    data = serializers.serialize('json', messages_from_chat)
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type="application/json")


def chat_ajax_send(request):
    owner = request.user
    message = request.GET['message']
    chat = Chat()
    chat.owner = owner
    chat.message = message
    chat.save()
    return JsonResponse({'ok': 'yuhuuu!!'})


def chat_ajax_user(request):
    user_id = int(request.GET['userID'])
    user = User.objects.get(id=user_id)
    data = serializers.serialize('json', [user])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type="application/json")