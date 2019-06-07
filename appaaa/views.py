import datetime

from django_user_agents.utils import get_user_agent

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.base import View
from django.contrib.gis.geoip2 import GeoIP2

from appaaa.models import Feedback, Comment
from appblog.models import Article
from appmail.views import manager_send_mail, writer_send_mail
from apporders.models import TypeOrder, PriceDeadline, Order, FeedbackOrder
from appusers.models import User


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

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('HTTP_X_REAL_IP')

        g = GeoIP2()
        geo = g.city(ip)

        ug = get_user_agent(request)

        feedback = Feedback()
        feedback.name = name
        feedback.email = email
        feedback.subject = subject
        feedback.message = message

        feedback.ip = ip
        feedback.country = geo['country_name']
        feedback.city = geo['city']
        feedback.time_zone = geo['time_zone']

        if ug.is_mobile:
            feedback.device = 'Mobile'
        elif ug.is_tablet:
            feedback.device = 'Tablet'
        elif ug.is_touch_capable:
            feedback.device = 'Touch capable'
        elif ug.is_pc:
            feedback.device = 'PC'
        elif ug.is_bot:
            feedback.device = 'Bot'
        else:
            feedback.device = 'Unknown'

        feedback.browser = F'{ug.browser.family} {ug.browser.version_string}'
        feedback.operation_system = F'{ug.os.family} {ug.os.version_string}'

        feedback.save()
        manager_send_mail('New feedback from site', name, subject, 'dashboard/others/')
        messages.success(request, 'Ваше сообщение отправлено (перевести)')
        return redirect('/')
    else:
        messages.error(request, 'Данный страницы не существует (перевести)')
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


def order_feedback(request):
    order_id = int(request.GET['orderID'])
    stars = int(request.GET['stars'])

    order = Order.objects.get(id=order_id)
    feedback_order = FeedbackOrder()
    feedback_order.order = order
    feedback_order.rating = stars
    if 'txt' in request.GET:
        feedback_order.text = request.GET['txt']
    feedback_order.save()
    messages.success(request, 'Спасибо за ваш отзыв (перевести)')

    manager_send_mail('Rating order', order.customer, order.title, 'dashboard/m/order/{}/'.format(order_id))
    writer_send_mail('Rating order', order.title, 'dashboard/w/order/completed-{}/'.format(order_id))

    data = {'ok': 'good'}
    return JsonResponse(data)


def add_comment(request):
    if request.method == 'GET':
        messages.error(request, 'Доступ ограничен (перевести)')
        return redirect('/')
    if request.method == 'POST':
        user = User.objects.get(email=request.user)
        comment_obj = Comment()
        comment_obj.user = user
        comment_obj.comment = request.POST['comment']
        comment_obj.save()
        messages.success(request, 'Спасибо за ваш отзыв (перевести)')
        return redirect('/')
