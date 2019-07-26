import datetime
import decimal
import json

from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import make_aware
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from appaaa.models import Comment
from appblog.forms import ArticleForm
from appcourses.forms import TaskForm
from appcourses.models import Course, Task, TaskFile
from appdashboard.views import access_to_manager_and_admin
from appmail.views import customer_send_mail, notification_to_writer
from apporders.models import Order, Chat, TypeOrder, FormatOrder, PriceDeadline, FilterWord
from appusers.forms import UserForm
from appusers.models import User, ChatUser, MessageChatUser, FileChatUser

check_is_manager = user_passes_test(lambda user: user.groups.all()[0].name == 'Manager' if user.is_authenticated else False)


def to_datetime(_datetime):
    # 2019-06-30T12:12
    dt = _datetime.split('T')  # ['2019-06-30', '12:12']
    d = [int(d) for d in dt[0].split('-')]  # [2019, 06, 30]
    t = [int(t) for t in dt[1].split(':')]  # [12, 12]
    format_date = datetime.datetime(d[0], d[1], d[2], t[0], t[1])
    aware_datetime = make_aware(format_date)
    return aware_datetime


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


@check_is_manager
def index(request):
    return redirect('/m/orders/')


@check_is_manager
def orders(request):
    _orders = Order.objects.all()
    in_review = _orders.filter(status__in=[0, 3])
    in_process = _orders.filter(status=1)
    completed = _orders.filter(status=2).order_by('-completed_datetime')
    context = {
        'in_review': in_review,
        'in_process': in_process,
        'completed': completed,
    }
    return render(request, 'dashboard-v2/m/orders/tabs.html', context=context)


@check_is_manager
def order_preview(request, pk):
    if request.method == 'GET':
        order = get_object_or_404(Order, id=pk, status__in=[0, 3])

    if request.method == 'POST':
        order = Order.objects.get(id=pk)
        if order.status == 3:
            order.status = 0
            order.save()

    return render(request, 'dashboard-v2/m/orders/detail/preview.html', context={'order': order})


@check_is_manager
def order_in_process(request, pk):
    order = get_object_or_404(Order, id=pk, status=1)

    if request.method == 'POST':
        message_id = request.POST.get('message_id', None)
        if message_id is not None:
            message = Chat.objects.get(id=int(message_id))
            message.status = True
            message.save()

    return render(request, 'dashboard-v2/m/orders/detail/in-process.html', context={'order': order})


@check_is_manager
def order_completed(request, pk):
    order = get_object_or_404(Order, id=pk, status=2)
    return render(request, 'dashboard-v2/m/orders/detail/completed.html', context={'order': order})


@check_is_manager
def courses(request):
    user = User.objects.get(email=request.user)
    all_courses = Course.objects.filter(Q(manager=None) | Q(manager=user))
    tasks = Task.objects.exclude(price_status=1)
    in_review = tasks.filter(status=0)
    in_process = tasks.filter(status=1)
    completed = tasks.filter(status=2)
    context = {
        'all_courses': all_courses,
        'in_review': in_review,
        'in_process': in_process,
        'completed': completed,
    }
    return render(request, 'dashboard-v2/m/courses/tabs.html', context=context)


@check_is_manager
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
    context = {
        'user_form': user_form,
        'change_password': change_password
    }
    return render(request, 'dashboard-v2/m/settings/tabs.html', context=context)


@check_is_manager
def course_detail(request, pk):
    course = Course.objects.get(id=pk)

    if request.method == 'POST':
        if 'send_customer' in request.POST:
            task = Task.objects.get(id=int(request.POST['send_customer']))
            task.price_status = 1
            task.save()
            customer_send_mail('New task in course', task.course.title, task.course.customer.email, F'/c/courses/detail/{task.course.id}/')
        else:
            form = TaskForm(request.POST)
            attached_files = request.FILES.getlist('attached-files')
            dt = to_datetime(request.POST['due_date'])
            if form.is_valid():
                cd = form.cleaned_data
                task = Task()
                task.course = course
                task.title = cd['title']
                task.due_date = dt
                task.question = cd['question']
                task.pages = cd['pages']
                task.description = cd['description']
                task.price_for_customer = cd['price_for_customer']
                if cd['to_writer']:
                    task.to_writer = cd['to_writer']
                    task.price_for_writer = cd['price_for_writer']
                task.save()
                if len(attached_files) != 0:
                    for f in attached_files:
                        file = TaskFile()
                        file.task = task
                        file.file = f
                        file.save()
                messages.success(request, 'Added new task')
                return redirect('/m/courses/detail/{}/'.format(pk))
            else:
                messages.error(request, 'The fields are incorrectly filled')

    return render(request, 'dashboard-v2/m/courses/course/course-detail.html', context={'course': course})


@check_is_manager
def users(request):
    _users = User.objects.all()
    customers = _users.filter(groups__name='Customer')
    writers = _users.filter(groups__name='Writer')
    context= {
        'customers': customers,
        'writers': writers,
        '_users': _users,
    }
    return render(request, 'dashboard-v2/m/users/tabs.html', context=context)


@check_is_manager
def users_customer(request, pk):
    customer = User.objects.get(id=pk)
    orders = Order.objects.filter(customer=customer)
    in_review = orders.filter(status__in=[0, 3])
    in_progress = orders.filter(status=1)
    completed = orders.filter(status=2)
    context = {
        'customer': customer,
        'orders': orders,
        'in_review': in_review,
        'in_progress': in_progress,
        'completed': completed
    }
    return render(request, 'dashboard-v2/m/users/customer/tabs.html', context=context)


@check_is_manager
def users_writer(request, pk):
    writer = User.objects.get(id=pk)
    orders = Order.objects.filter(writer=writer)
    in_progress = orders.filter(status=1)
    completed = orders.filter(status=2)
    context = {
        'writer': writer,
        'orders': orders,
        'in_progress': in_progress,
        'completed': completed,
    }
    return render(request, 'dashboard-v2/m/users/writer/tabs.html', context=context)


@check_is_manager
def type_order(request):
    types_order = TypeOrder.objects.all()

    if request.method == 'POST':
        if request.is_ajax():
            title = request.POST['title']
            price_customer = request.POST['priceCustomer']
            price_writer = request.POST['priceWriter']
            if request.POST['action'] == 'add':
                to = TypeOrder()
                to.title = title
                to.price_client = price_customer
                to.price_writer = price_writer
                to.save()

            to = TypeOrder.objects.get(title=title)
            if request.POST['action'] == 'edit':
                to.price_client = price_customer
                to.price_writer = price_writer
                to.save()

            if request.POST['action'] == 'delete':
                to.delete()

            return JsonResponse({'ok': 'yes'})
        else:
            messages.error(request, 'Неверный запрос')
            return redirect('/')

    return render(request, 'dashboard-v2/m/selects/type-order.html', context={'types_order': types_order})


@check_is_manager
def format_order(request):
    formats_order = FormatOrder.objects.all()

    if request.method == 'POST':
        if request.is_ajax():
            title = request.POST['title']

            if request.POST['action'] == 'add':
                fo = FormatOrder()
                fo.title = title
                fo.save()

            fo = FormatOrder.objects.get(title=title)
            if request.POST['action'] == 'edit':
                fo.title = request.POST['newTitle']
                fo.save()

            if request.POST['action'] == 'delete':
                fo.delete()

            return JsonResponse({'ok': 'yes'})
        else:
            messages.error(request, 'Invalid request')
            return redirect('/')

    return render(request, 'dashboard-v2/m/selects/format-order.html', context={'formats_order': formats_order})


@check_is_manager
def deadline(request):
    deadlines = PriceDeadline.objects.all()

    if request.method == 'POST':
        if request.is_ajax():
            price = decimal.Decimal(request.POST['price'].split('$')[-1])

            if request.POST['action'] == 'add':
                dl = PriceDeadline()
                if request.POST['day'] != '':
                    dl.days = int(request.POST['day'])
                if request.POST['hour'] != '':
                    dl.hours = int(request.POST['hour'])
                dl.price = price
                dl.save()

            dl = PriceDeadline.objects.get(price=price)
            if request.POST['action'] == 'edit':
                dl.days = int(request.POST['day'])
                dl.hours = int(request.POST['hour'])
                dl.price = decimal.Decimal(request.POST['newPrice'].split('$')[-1])
                dl.save()

            if request.POST['action'] == 'delete':
                dl.delete()

            return JsonResponse({'ok': 'yes'})
        else:
            messages.error(request, 'Invalid request')
            return redirect('/')

    return render(request, 'dashboard-v2/m/selects/deadline.html', context={'deadlines': deadlines})


@check_is_manager
def filter_words(request):
    fws = FilterWord.objects.all()

    if request.method == 'POST':
        if request.is_ajax():
            word = request.POST['word']

            if request.POST['action'] == 'add':
                fw = FilterWord()
                fw.word = word
                fw.save()

            fw = FilterWord.objects.get(word=word)
            if request.POST['action'] == 'edit':
                fw.word = request.POST['newWord']
                fw.save()

            if request.POST['action'] == 'delete':
                fw.delete()

            return JsonResponse({'ok': 'yes'})
        else:
            messages.error(request, 'Invalid request')
            return redirect('/')

    return render(request, 'dashboard-v2/m/others/filter-words.html', context={'fws': fws})


@check_is_manager
def testimonials(request):
    tms = Comment.objects.all().order_by('-id')

    if request.method == 'POST':
        if request.is_ajax():
            checked = True if request.POST['checked'] == 'true' else False

            if request.POST['action'] == 'add':
                c = Comment()
                if request.POST['fullName'] != '':
                    c.full_name = request.POST['fullName']
                if request.POST['academicInstitution'] != '':
                    c.academic_institution = request.POST['academicInstitution']
                c.comment = request.POST['comment']
                c.checked = checked
                c.save()

            comment = request.POST['comment']
            c = Comment.objects.get(comment=comment)
            if request.POST['action'] == 'edit':
                c.full_name = request.POST['fullName']
                c.academic_institution = request.POST['academicInstitution']
                c.comment = request.POST['newComment']
                c.checked = checked
                c.save()
            if request.POST['action'] == 'delete':
                c.delete()

            return JsonResponse({'ok': 'yes'})

    return render(request, 'dashboard-v2/m/others/testimonials.html', context={'tms': tms})


@check_is_manager
def add_article(request):
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article successfully added')
            return redirect('/m/add-article/')
        else:
            form = ArticleForm(request.POST, request.FILES)
            messages.error(request, 'Invalid fields')

    return render(request, 'dashboard-v2/m/others/add-article.html', context={'form': form})


@check_is_manager
def writer_chat(request, pk):
    if request.method == 'GET':
        chat = ChatUser.objects.get(id=pk)
        messages_from_chat = MessageChatUser.objects.filter(chat=chat).order_by('-id')
        files_from_chat = FileChatUser.objects.filter(chat=chat).order_by('-id')
        if request.is_ajax():
            r_mfc = request.GET.get('messagesFromChat', None)
            r_ffc = request.GET.get('filesFromChat', None)
            r_snm = request.GET.get('sendNotificationMail', None)

            if r_snm is not None:
                # t = request.META['HTTP_REFERER'].split('/')[3::]
                # t.pop()  # t == ['m', 'chat', '3']
                writer_email = chat.user.email
                notification_to_writer(F'w/chat/{pk}/', writer_email)

            # Вывод сообщений из чата
            if r_mfc is not None:
                messages_chat = MessageChatUser.objects.filter(chat=chat).order_by('id')
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
                files_chat = FileChatUser.objects.filter(chat=chat).order_by('id')
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
                        'link': F'{file.file.url}',
                        'created_datetime': created_datetime,
                    }
                    obj_files.append(_dict)

                data = json.dumps(obj_files)
                return HttpResponse(data, content_type="application/json")

        if access_to_manager_and_admin(request.user):
            context = {
                'chat': chat,
                'messages_from_chat': messages_from_chat,
                'files_from_chat': files_from_chat,
                'btn_notification': True
            }
            return render(request, 'dashboard-v2/m/chat/main.html', context=context)
        else:
            return redirect(F'/m/chat/{chat.id}/')

    if request.method == 'POST':
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
