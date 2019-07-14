import datetime
import json

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from appcourses.models import Course, Task, TaskFileCompleted
from appdashboard.views import access_to_manager_and_admin
from appmail.views import manager_send_mail, customer_send_mail
from apporders.models import Order, AdditionallyOrder, Chat, FilesAdditionallyOrder
from apporders.validators import validate_file_views
from appusers.forms import UserCustomerForm
from appusers.models import User, ChatUser, MessageChatUser, FileChatUser


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


def index(request):

    return render(request, 'dashboard-v2/w/index.html', locals())


def orders(request):
    user = User.objects.get(email=request.user)

    if request.method == 'GET':
        if request.user.groups.all()[0].name == 'Writer':
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
                    return redirect(F'/w/orders/inprocess/{pk}/')
                file_additional = FilesAdditionallyOrder()
                file_additional.additionally_order = additionally_order
                file_additional.file = f
                file_additional.save()
            customer_send_mail('New files', order.title, order.customer.email, F'/c/orders/inprocess/{order.id}/')
            manager_send_mail('New files', order.writer, order.title, F'm/orders/preview/{order.id}/')
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
    tasks = Task.objects.filter(Q(price_status=2) & Q(to_writer=True))
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


def task_inprocess(request, pk):
    user = User.objects.get(email=request.user)
    task = Task.objects.get(id=pk, price_status=2, status=1, writer=user)

    if request.method == 'POST':
        if 'files' in request.FILES:
            req_files = request.FILES.getlist('files')
            for f in req_files:
                if validate_file_views(f) == 'error':
                    messages.error(request, 'Invalid format loaded')
                    return redirect('/w/courses/task/inprocess/{}/'.format(pk))
                task_file_completed = TaskFileCompleted()
                task_file_completed.task = task
                task_file_completed.file = f
                task_file_completed.save()
            customer_send_mail('New files', task.title, task.course.customer.email, F'c/courses/task/inprocess/{task.id}/')
            manager_send_mail('New files', task.writer, task.title, F'm/courses/task/inprocess/{task.id}/')
            messages.success(request, 'Files uploaded successfully')
            return redirect(F'/w/courses/task/inprocess/{task.id}/')

    return render(request, 'dashboard-v2/w/courses/course/task-inprocess.html', locals())


def task_detail(request, pk):
    user = User.objects.get(email=request.user)
    task = Task.objects.get(id=pk, price_status=2, status=0)

    if request.method == 'POST':
        r = request.POST
        take = r.get('take', None)

        if take is not None:
            task = Task.objects.get(id=int(take))
            task.writer = user
            task.status = 1
            task.save()
            # TODO: Написать уведомление на почту менеджеру и кастомеру о принятии заказа

    return render(request, 'dashboard-v2/w/courses/course/task-detail.html', locals())


class ChatViews(View):

    @staticmethod
    def get(request, pk):

        if request.user.is_anonymous:
            messages.error(request, 'Access is limited')
            return redirect('/')
        user = User.objects.get(email=request.user)
        chat = ChatUser.objects.get(id=pk, user=user)
        messages_from_chat = MessageChatUser.objects.filter(chat=chat).order_by('-id')
        files_from_chat = FileChatUser.objects.filter(chat=chat).order_by('-id')

        if request.is_ajax():
            r_mfc = request.GET.get('messagesFromChat', None)
            r_ffc = request.GET.get('filesFromChat', None)

            # Вывод сообщений из чата
            if r_mfc is not None:
                messages_chat = MessageChatUser.objects.filter(chat=chat)
                obj_messages = []
                for message in messages_chat:
                    created_datetime = '{}:{} {}.{}.{}'.format(
                        message.created_time.hour, message.created_time.minute,
                        message.created_date.day, message.created_date.month, message.created_date.year
                    )
                    updated_datetime = '{}:{} {}.{}.{}'.format(
                        message.updated_time.hour, message.updated_time.minute,
                        message.updated_date.day, message.updated_date.month, message.updated_date.year
                    )
                    _dict = {
                        'avatar': message.owner.avatar.url if message.owner.avatar else '/static/img/noimage.png',
                        'owner': message.owner.get_full_name() if message.owner.get_full_name else message.owner.email,
                        'message': message.message,
                        'created_datetime': created_datetime,
                        'updated_datetime': updated_datetime,
                    }
                    obj_messages.append(_dict)

                data = json.dumps(obj_messages)
                return HttpResponse(data, content_type="application/json")

            # Вывод файлов из чата
            if r_ffc is not None:
                files_chat = FileChatUser.objects.filter(chat=chat)
                obj_files = []
                for file in files_chat:
                    created_datetime = '{}:{} {}.{}.{}'.format(
                        file.created_time.hour, file.created_time.minute,
                        file.created_date.day, file.created_date.month, file.created_date.year
                    )
                    _dict = {
                        'avatar': file.owner.avatar.url if file.owner.avatar else '/static/img/noimage.png',
                        'owner': file.owner.get_full_name() if file.owner.get_full_name else file.owner.email,
                        'name': file.filename(),
                        'link': F'{file.file}',
                        'created_datetime': created_datetime,
                    }
                    obj_files.append(_dict)

                data = json.dumps(obj_files)
                return HttpResponse(data, content_type="application/json")

        if access_to_manager_and_admin(request.user) or chat.user == user:
            context = {
                'chat': chat,
                'messages_from_chat': messages_from_chat,
                'files_from_chat': files_from_chat
            }
            return render(request, 'dashboard-v2/w/chat/main.html', context=context)
        else:
            return redirect(F'/w/chat/{request.user.chatuser.id}/')

    @staticmethod
    def post(request, pk):
        if request.is_ajax():
            message = request.POST['message']
            files = request.FILES.getlist('files[]')
            chat = ChatUser.objects.get(id=pk)
            user = User.objects.get(email=request.user)

            if len(files) != 0:
                for f in files:
                    print(f)
                    file = FileChatUser()
                    file.chat = chat
                    file.owner = user
                    file.file = f
                    file.save()

            if message != '':
                message_chat = MessageChatUser()
                message_chat.owner = user
                message_chat.chat = chat
                message_chat.message = message
                message_chat.save()

                return JsonResponse({'ok': 'asd'})

            return JsonResponse({'error': 'Not message'})

        else:
            messages.error(request, 'This is not ajax request')
