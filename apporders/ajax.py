from django.http import JsonResponse

from appmail.views import customer_send_mail, writer_send_mail
from apporders.models import Chat


def chat_message_accept(request):
    message_id = request.GET['messageID']
    message = Chat.objects.get(id=message_id)
    message.status = True
    message.save()

    order = message.order
    writer_link_order = F'dashboard/w/order/{order.id}/'
    customer_link_order = F'orders/progress/{order.id}/'

    groups = message.user.groups.all()
    for g in groups:
        if g.name == 'Customer':
            customer_send_mail('New message in order', order.title, order.customer.email, customer_link_order)
        if g.name == 'Writer':
            writer_send_mail('New message in order', order.title, writer_link_order)

    data = {'ok': 'yeee!!'}
    return JsonResponse(data=data)
