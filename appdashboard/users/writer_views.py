import datetime

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from appcourses.models import Course, Task
from appdashboard.views import access_to_manager_and_admin
from appmail.views import manager_send_mail, customer_send_mail
from apporders.models import Order, AdditionallyOrder, Chat, FilesAdditionallyOrder
from apporders.validators import validate_file_views
from appusers.forms import UserCustomerForm
from appusers.models import User


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


def index(request):

    return render(request, 'dashboard-v2/w/index.html', locals())


def orders(request):
    user = User.objects.get(email=request.user)

    if request.method == 'GET':
        if access_to_manager_and_admin(user):
            # TODO: Необходимо получить инфу о customer
            _orders = Order.objects.all()
        elif request.user.groups.all()[0].name == 'Writer':
            _orders = Order.objects.all()
        else:
            return redirect('/')
        in_review = _orders.filter(status=0)
        in_process = _orders.filter(status=1)
        completed = _orders.filter(status=2).order_by('-completed_datetime')

    return render(request, 'dashboard-v2/w/orders/tabs.html', locals())


def order_preview(request, pk):
    order = get_object_or_404(Order, id=pk, status=0)
    if request.method == 'POST':
        user = User.objects.get(email=request.user)
        order = Order.objects.get(id=pk)
        if order.status == 0:
            order.status = 1
            order.writer = user
            order.save()
            try:
                additional = AdditionallyOrder.objects.get(order=order)
            except AdditionallyOrder.DoesNotExist:
                additional = AdditionallyOrder()
                additional.order = order
                additional.save()
            messages.success(request, 'You have successfully accepted the order')
            return redirect(F'/w/orders/inprocess/{pk}/')
        else:
            messages.warning(request, 'The order has already been accepted by another writer.')

    return render(request, 'dashboard-v2/w/orders/detail/preview.html', locals())


def order_in_process(request, pk):
    user = User.objects.get(email=request.user)
    if request.method == 'GET':
        order = get_object_or_404(Order, id=pk, status=1, writer=user)

        return render(request, 'dashboard-v2/w/orders/detail/in-process.html', context={'order': order})

    if request.method == 'POST':
        order = Order.objects.get(id=pk, writer=user)

        if 'message' in request.POST and request.POST['message'] != '':
            chat = Chat()
            chat.order = order
            chat.user = user
            chat.message = request.POST['message']
            chat.status = False
            chat.save()
            manager_send_mail('New message from chat', order.customer, order.title, F'/m/orders/inprocess/{order.id}/')
            messages.success(request, 'Your message has been sent.')
            return redirect(F'/w/orders/inprocess/{pk}/')

        try:
            additionally_order = AdditionallyOrder.objects.get(order=order)
        except AdditionallyOrder.DoesNotExist:
            additionally_order = AdditionallyOrder()
            additionally_order.order = order
            additionally_order.save()

        if 'files' in request.FILES:
            req_files = request.FILES.getlist('files')
            for f in req_files:
                if validate_file_views(f) == 'error':
                    messages.error(request, 'Invalid format loaded')
                    return redirect('/dashboard/')
                file_additional = FilesAdditionallyOrder()
                file_additional.additionally_order = additionally_order
                file_additional.file = f
                file_additional.save()
            customer_send_mail('New files', order.title, order.customer.email, F'/c/orders/inprocess/{order.id}/')
            manager_send_mail('New files', order.writer, order.title, F'dashboard/m/order/{order.id}/')
            messages.success(request, 'Files uploaded successfully')
            return redirect(F'/w/orders/inprocess/{pk}/')

        if 'message' in request.POST and request.POST['message'] != '':
            chat = Chat()
            chat.order = order
            chat.user = user
            chat.message = request.POST['message']
            chat.status = False
            chat.save()

            manager_send_mail('New message from chat', order.writer, order.title, F'/m/orders/inprocess/{order.id}/')
            messages.success(request, 'Your message has been sent.')
            return redirect(F'/w/orders/inprocess/{pk}/')
        else:
            messages.success(request, 'Message cannot be empty')
            return redirect(F'/w/orders/inprocess/{pk}/')


def order_completed(request, pk):
    user = User.objects.get(email=request.user)
    order = get_object_or_404(Order, id=pk, status=2, writer=user)
    return render(request, 'dashboard-v2/w/orders/detail/completed.html', locals())


def courses(request):
    user = User.objects.get(email=request.user)
    tasks = Task.objects.exclude(Q(price_status=1) & Q(to_writer=False))
    in_review = tasks.filter(status=0)
    in_process = tasks.filter(status=1)
    completed = tasks.filter(status=2)

    return render(request, 'dashboard-v2/w/courses/tabs.html', locals())


def settings(request):
    user = User.objects.get(email=request.user)
    user_form = UserCustomerForm(instance=user)
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
            return redirect('/w/settings/')

        if _change_password is not None:
            change_password = PasswordChangeForm(user, request.POST)
            if change_password.is_valid():
                change_password.save()
                messages.success(request, 'Your password has been successfully changed.')
                return redirect('/w/settings/')
            else:
                messages.error(request, 'Invalid fields')
                return redirect('/w/settings/')

    return render(request, 'dashboard-v2/w/settings/tabs.html', locals())


def detail(request, pk):
    course = Course.objects.get(id=pk)

    return render(request, 'dashboard-v2/w/courses/course/detail.html', locals())
