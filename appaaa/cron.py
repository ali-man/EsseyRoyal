import datetime

from django.shortcuts import render

from appmail.views import writer_rest_of_time_send_mail, manager_rest_of_time_send_mail
from apporders.models import Order


def to_order_deadline(order):
    _date = order.deadline.date()
    _time = order.deadline.time()
    order_deadline = datetime.datetime(
        _date.year,
        _date.month,
        _date.day,
        _time.hour,
        _time.minute
    )
    return order_deadline


def rest_of_time(order):
    today = datetime.datetime.now()
    order_deadline = to_order_deadline(order)
    deadline = (order_deadline - today).total_seconds()
    hours = divmod(deadline, 3600)[0]
    return int(hours)


def mailing(order, hours):
    writer_rest_of_time_send_mail(
        F'Less than {hours} hours left',
        order.title,
        order.id,
        order.writer.email
    )
    manager_rest_of_time_send_mail(
        F'Less than {hours} hours left',
        order.title,
        order.id,
    )


def search_deadline(request):
    orders = Order.objects.filter(status=1)

    for order in orders:
        hours = rest_of_time(order)
        if hours <= 24:
            mailing(order, 24)

    return render(request, 'cron.html', context={'orders': orders})
