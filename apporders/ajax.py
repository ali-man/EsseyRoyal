from django.http import JsonResponse

from apporders.models import Chat


def chat_message_accept(request):
    message_id = request.GET['messageID']
    message = Chat.objects.get(id=message_id)
    message.status = True
    message.save()
    groups = message.user.groups.all()
    for g in groups:
        if g.name == 'Customer':
            pass # TODO: отправка письма клиенту о новом сообщении
        if g.name == 'Writer':
            pass # TODO: отправка письма писателя о новом сообщении

    data = {'ok': 'yeee!!'}
    return JsonResponse(data=data)
