from django.http import JsonResponse

from apporders.models import Chat


def chat_message_accept(request):
    message_id = request.GET['messageID']
    message = Chat.objects.get(id=message_id)
    message.status = True
    message.save()
    data = {'ok': 'yeee!!'}
    return JsonResponse(data=data)
