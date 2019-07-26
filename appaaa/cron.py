import datetime

from django.shortcuts import render

from appmail.views import writer_rest_of_time_send_mail, manager_rest_of_time_send_mail, banned_words_in_order, changed_status_of_order
from apporders.models import Order, SearchWord, checking_files


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


def check_order(request):
    orders = Order.objects.filter(status=3, checking=False)
    for order in orders:
        banned_word_description = False
        banned_word_files = False

        if len(order.description) != 0:  # Если в description есть текст
            sw = SearchWord()
            banned_words = sw.search_word(order.description)  # Проверка на фильтр слов
            if len(banned_words) != 0:  # Если найдены слова
                banned_word_description = True

        for file in order.filesorder_set.all():
            banned_words = checking_files(file.file)
            if len(banned_words) != 0:
                banned_word_files = True

        if (banned_word_description == False) and (banned_word_files == False):
            order.status = 0
            order.checking = True
            order.save()
            changed_status_of_order(order.id)
        else:
            order.checking = True
            order.save()
            banned_words_in_order(order.id)
    return render(request, 'cron.html', context={'orders': orders})
