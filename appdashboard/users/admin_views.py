import datetime
import decimal
import json

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from appaaa.models import Comment
from appblog.forms import ArticleForm
from appcourses.models import Course, Task
from appdashboard.views import access_to_manager_and_admin
from apporders.models import Order, Chat, TypeOrder, FormatOrder, PriceDeadline, FilterWord
from appusers.forms import UserForm, CreateUserForm
from appusers.models import User, ChatUser, FileChatUser, MessageChatUser


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


def index(request):
    return render(request, 'dashboard-v2/a/index.html', locals())


def orders(request):
    _orders = Order.objects.all()
    in_review = _orders.filter(status__in=[0, 3])
    in_process = _orders.filter(status=1)
    completed = _orders.filter(status=2).order_by('-completed_datetime')

    return render(request, 'dashboard-v2/a/orders/tabs.html', locals())


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

    return render(request, 'dashboard-v2/a/orders/detail/preview.html', locals())


def order_in_process(request, pk):
    order = get_object_or_404(Order, id=pk, status=1)

    if request.method == 'POST':
        message_id = request.POST.get('message_id', None)
        if message_id is not None:
            message = Chat.objects.get(id=int(message_id))
            message.status = True
            message.save()

    return render(request, 'dashboard-v2/a/orders/detail/in-process.html', context={'order': order})


def order_completed(request, pk):
    if not access_to_manager_and_admin(request.user):
        messages.error(request, 'Access closed')
        return redirect('/')
    order = get_object_or_404(Order, id=pk, status=2)
    return render(request, 'dashboard-v2/a/orders/detail/completed.html', locals())


def courses(request):
    user = User.objects.get(email=request.user)
    all_courses = Course.objects.filter(Q(manager=None) | Q(manager=user))
    tasks = Task.objects.exclude(price_status=1)
    in_review = tasks.filter(status=0)
    in_process = tasks.filter(status=1)
    completed = tasks.filter(status=2)

    return render(request, 'dashboard-v2/a/courses/tabs.html', locals())


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
            return redirect('/a/settings/')

        if _change_password is not None:
            change_password = PasswordChangeForm(user, request.POST)
            if change_password.is_valid():
                change_password.save()
                messages.success(request, 'Your password has been successfully changed.')
                return redirect('/a/settings/')
            else:
                messages.error(request, 'Invalid fields')
                return redirect('/a/settings/')

    return render(request, 'dashboard-v2/a/settings/tabs.html', locals())


def detail(request, pk):
    course = Course.objects.get(id=pk)

    return render(request, 'dashboard-v2/a/courses/course/detail.html', locals())


def users(request):
    _users = User.objects.all()
    customers = _users.filter(groups__name='Customer')
    writers = _users.filter(groups__name='Writer')
    new_user = CreateUserForm()

    if request.method == 'POST':
        if '1' == request.POST['select_user']:
            form_writer = CreateUserForm(request.POST, request.FILES)
            if form_writer.is_valid():
                cd = form_writer.cleaned_data
                g = Group.objects.get(name='Writer')
                user = User()
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.email = cd['email']
                user.set_password(cd['password'])
                user.corporate_email = cd['corporate_email']
                user.phone = cd['phone']
                user.academic_institution = cd['academic_institution']
                user.degree = cd['degree']
                user.avatar = cd['avatar']
                user.save()
                user.groups.add(g)
                user.save()
                chat = ChatUser()
                chat.user = user
                chat.save()
                messages.success(request, 'Новый врайтер успешно создан (певести)')
                return redirect('/a/users/')
            else:
                messages.error(request, 'Неверно заполнены поля (певести)')
                return redirect('/a/users/')

        if '2' == request.POST['select_user']:
            create_manager = CreateUserForm(request.POST, request.FILES)
            if create_manager.is_valid():
                cd = create_manager.cleaned_data
                g = Group.objects.get(name='Manager')
                user = User()
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.email = cd['email']
                user.set_password(cd['password'])
                user.corporate_email = cd['corporate_email']
                user.phone = cd['phone']
                user.academic_institution = cd['academic_institution']
                user.degree = cd['degree']
                user.avatar = cd['avatar']
                user.save()
                user.groups.add(g)
                user.save()
                messages.success(request, 'Новый manager успешно создан (певести)')
                return redirect('/a/users/')
            else:
                messages.error(request, 'Неверно заполнены поля (певести)')
                return redirect('/a/users/')

    return render(request, 'dashboard-v2/a/users/tabs.html', locals())


def users_customer(request, pk):
    customer = User.objects.get(id=pk)
    orders = Order.objects.filter(customer=customer)
    in_review = orders.filter(status__in=[0, 3])
    in_progress = orders.filter(status=1)
    completed = orders.filter(status=2)
    return render(request, 'dashboard-v2/a/users/customer/tabs.html', locals())


def users_writer(request, pk):
    writer = User.objects.get(id=pk)
    orders = Order.objects.filter(writer=writer)
    in_progress = orders.filter(status=1)
    completed = orders.filter(status=2)
    return render(request, 'dashboard-v2/a/users/writer/tabs.html', locals())


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

    return render(request, 'dashboard-v2/a/selects/type-order.html', locals())


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

    return render(request, 'dashboard-v2/a/selects/format-order.html', locals())


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

    return render(request, 'dashboard-v2/a/selects/deadline.html', locals())


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

    return render(request, 'dashboard-v2/a/others/filter-words.html', locals())


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

    return render(request, 'dashboard-v2/a/others/testimonials.html', locals())


def add_article(request):
    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article successfully added')
            return redirect('/a/add-article/')
        else:
            form = ArticleForm(request.POST, request.FILES)
            messages.error(request, 'Invalid fields')

    return render(request, 'dashboard-v2/a/others/add-article.html', locals())


def writer_chat(request, pk):
    if request.method == 'GET':
        chat = ChatUser.objects.get(id=pk)
        messages_from_chat = MessageChatUser.objects.filter(chat=chat).order_by('-id')
        files_from_chat = FileChatUser.objects.filter(chat=chat).order_by('-id')
        if request.is_ajax():
            r_mfc = request.GET.get('messagesFromChat', None)
            r_ffc = request.GET.get('filesFromChat', None)

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
                        'link': F'{file.file}',
                        'created_datetime': created_datetime,
                    }
                    obj_files.append(_dict)

                data = json.dumps(obj_files)
                return HttpResponse(data, content_type="application/json")

        if access_to_manager_and_admin(request.user):
            context = {
                'chat': chat,
                'messages_from_chat': messages_from_chat,
                'files_from_chat': files_from_chat
            }
            return render(request, 'dashboard-v2/a/chat/main.html', context=context)
        else:
            return redirect(F'/a/chat/{chat.id}/')

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
