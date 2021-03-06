import datetime

from django_user_agents.utils import get_user_agent

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.base import View
from django.contrib.gis.geoip2 import GeoIP2

from appaaa.models import Feedback, Comment
from appmail.views import manager_send_mail, writer_send_mail, manager_send_mail_of_feedback
from apporders.models import TypeOrder, PriceDeadline, Order, FeedbackOrder, FilterWord
from appusers.models import User


class HomePageViews(View):
    @staticmethod
    def get(request):
        type_order = TypeOrder.objects.all()
        comments = Comment.objects.filter(checked=True).order_by('-id')
        comments_1 = comments[:3]
        comments_2 = comments[3:6]
        context = {
            'type_order': type_order,
            'comments': comments,
            'comments_1': comments_1,
            'comments_2': comments_2,
        }
        return render(request, 'home.html', context=context)


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

        fb = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'ip': ip,
            'country': geo['country_name'],
            'city': geo['city'],
            'time_zone': geo['time_zone'],
            'device': '',
            'browser': F'{ug.browser.family} {ug.browser.version_string}',
            'os': F'{ug.os.family} {ug.os.version_string}'
        }

        if ug.is_mobile:
            fb['device'] = 'Mobile'
        elif ug.is_tablet:
            fb['device'] = 'Tablet'
        elif ug.is_touch_capable:
            fb['device'] = 'Touch capable'
        elif ug.is_pc:
            fb['device'] = 'PC'
        elif ug.is_bot:
            fb['device'] = 'Bot'
        else:
            fb['device'] = 'Unknown'
        manager_send_mail_of_feedback(fb)
        messages.success(request, 'Your message has been sent.')
        return redirect('/')
    else:
        messages.error(request, 'This page does not exist.')
        return redirect('/')


def calculate_home(request):
    pages = 1
    type_order_int = int(request.GET['typeOrder'])  # 4
    if request.GET['pagesOrder'] != '':
        pages = int(request.GET['pagesOrder'])  # 4
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
    messages.success(request, 'Thanks for your feedback')

    manager_send_mail('Rating order', order.customer, order.title, F'm/orders/completed/{order.id}/')
    writer_send_mail('Rating order', order.title, F'w/orders/completed/{order.id}/', order.writer.email)

    data = {'ok': F'/c/orders/completed/{order_id}/'}
    return redirect(F'/c/orders/completed/{order_id}/')


def add_testimonial(request):
    if request.method == 'GET':
        messages.error(request, 'Access is limited')
        return redirect('/')
    if request.method == 'POST':
        user = User.objects.get(email=request.user)
        comment_obj = Comment()
        comment_obj.user = user
        comment_obj.comment = request.POST['comment']
        comment_obj.save()
        messages.success(request, 'Thanks for your feedback')
        return redirect('/c/orders/')


def add_word(request):
    if request.is_ajax():
        if request.POST['wordID'] == 'no':
            word = FilterWord()
            word.word = request.POST['word'].strip()
            word.save()
            return JsonResponse({'ok': 'create'})
        elif request.POST['wordID'] == 'remove':
            word_strip = request.POST['word'].strip()
            try:
                word = FilterWord.objects.get(word=word_strip)
                word.delete()
                return JsonResponse({'ok': 'remove'})
            except FilterWord.DoesNotExist:
                pass
        else:
            word = FilterWord.objects.get(id=int(request.POST['wordID']))
            word.word = request.POST['word'].strip()
            word.save()
            return JsonResponse({'ok': 'edit'})
