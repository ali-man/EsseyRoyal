import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.base import View

from appaaa.models import Feedback
from appblog.models import Article
from apporders.models import TypeOrder, PriceDeadline


class HomePageViews(View):
    @staticmethod
    def get(request):
        type_order = TypeOrder.objects.all()

        return render(request, 'home.html', locals())


def comment(request):
    if request.method == 'POST':
        return redirect('/')


def feedback(request):
    if request.method == 'POST':
        r = request.POST
        name = r['name']
        email = r['email']
        subject = r['subject']
        message = r['message']
        feedback = Feedback()
        feedback.name = name
        feedback.email = email
        feedback.subject = subject
        feedback.message = message
        feedback.save()
        messages.success(request, 'Ваше сообщение отправлено (перевести)')
        return redirect('/')


def calculate_home(request):
    type_order_int = int(request.GET['typeOrder']) # 4
    pages = int(request.GET['pagesOrder']) # 4
    date_str = request.GET['date'] # 30-05-2019
    time_str = request.GET['time'] # 17:30

    date_sort = list(map(int, date_str.split('-')))
    time_sort = list(map(int, time_str.split(':')))
    date = datetime.datetime(date_sort[2], date_sort[1], date_sort[0], time_sort[0], time_sort[1])

    type_order = TypeOrder.objects.get(id=type_order_int)

    deadline = (date - datetime.datetime.now()).total_seconds()
    hours = int(divmod(deadline, 3600)[0])
    deadlines_price = PriceDeadline.objects.filter(hours__lte=hours)
    last_index = len(deadlines_price) - 1  # Последний индекс из queryset
    price = deadlines_price[last_index].price + type_order.price_client  # Цена type of order
    per_page = price
    total_cost = price * pages
    data = {
        'per_page': per_page,
        'total_cost': total_cost
    }
    return JsonResponse(data)