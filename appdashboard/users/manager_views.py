import datetime

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from appcourses.models import Course, Task
from appdashboard.views import access_to_manager_and_admin
from apporders.models import Order, AdditionallyOrder, Chat
from appusers.forms import UserForm
from appusers.models import User


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


def index(request):

    return render(request, 'dashboard-v2/m/index.html', locals())


def orders(request):
    _orders = Order.objects.all()
    in_review = _orders.filter(status__in=[0, 3])
    in_process = _orders.filter(status=1)
    completed = _orders.filter(status=2)

    return render(request, 'dashboard-v2/m/orders/tabs.html', locals())


def order_preview(request, pk):
    if request.method == 'GET':
        if not access_to_manager_and_admin(request.user):
            messages.error(request, 'Access closed')
            return redirect('/')

        order = get_object_or_404(Order, id=pk, status__in=[0, 3])

    if request.method == 'POST':
        order = Order.objects.get(id=pk)
        if order.status == 3:
            order.status = 0
            order.save()

    return render(request, 'dashboard-v2/m/orders/detail/preview.html', locals())


def order_in_process(request, pk):
    order = get_object_or_404(Order, id=pk, status=1)

    if request.method == 'POST':
        message_id = request.POST.get('message_id', None)
        if message_id is not None:
            message = Chat.objects.get(id=int(message_id))
            message.status = True
            message.save()

    return render(request, 'dashboard-v2/m/orders/detail/in-process.html', context={'order': order})


def order_completed(request, pk):
    order = get_object_or_404(Order, id=pk, status=2)
    return render(request, 'dashboard-v2/m/orders/detail/completed.html', locals())


def courses(request):
    user = User.objects.get(email=request.user)
    all_courses = Course.objects.filter(Q(manager=None) | Q(manager=user))
    tasks = Task.objects.exclude(price_status=1)
    in_review = tasks.filter(status=0)
    in_process = tasks.filter(status=1)
    completed = tasks.filter(status=2)

    return render(request, 'dashboard-v2/m/courses/tabs.html', locals())


def settings(request):
    user = User.objects.get(email=request.user)
    user_form = UserForm(instance=user)
    change_password = PasswordChangeForm(user=user)

    if request.method == 'POST':
        r = request.POST
        _change_profile = r.get('_change_profile', None)
        _change_password = r.get('_change_password', None)
        if _change_profile is not None:
            user.first_name = r['first_name']
            user.last_name = r['last_name']
            user.academic_institution = r['academic_institution']
            user.degree = r['degree']
            user.phone = r['phone']
            if 'corporate_email' in r:
                user.corporate_email = r['corporate_email']
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            messages.success(request, 'Profile successfully changed')
            return redirect('/m/settings/')

        if _change_password is not None:
            change_password = PasswordChangeForm(user, request.POST)
            if change_password.is_valid():
                change_password.save()
                messages.success(request, 'Your password has been successfully changed.')
                return redirect('/m/settings/')
            else:
                messages.error(request, 'Invalid fields')
                return redirect('/m/settings/')

    return render(request, 'dashboard-v2/m/settings/tabs.html', locals())


def detail(request, pk):
    course = Course.objects.get(id=pk)

    return render(request, 'dashboard-v2/m/courses/course/detail.html', locals())
