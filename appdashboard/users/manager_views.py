import datetime
import decimal

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from appaaa.models import Comment
from appblog.forms import ArticleForm
from appcourses.models import Course, Task
from appdashboard.views import access_to_manager_and_admin
from apporders.models import Order, AdditionallyOrder, Chat, TypeOrder, FormatOrder, PriceDeadline, FilterWord
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
    completed = _orders.filter(status=2).order_by('-completed_datetime')

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
    if not access_to_manager_and_admin(request.user):
        messages.error(request, 'Access closed')
        return redirect('/')
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


def users(request):
    _users = User.objects.all()
    customers = _users.filter(groups__name='Customer')
    writers = _users.filter(groups__name='Writer')

    return render(request, 'dashboard-v2/m/users/tabs.html', locals())


def users_customer(request, pk):
    customer = User.objects.get(id=pk)
    orders = Order.objects.filter(customer=customer)
    in_review = orders.filter(status__in=[0, 3])
    in_progress = orders.filter(status=1)
    completed = orders.filter(status=2)
    return render(request, 'dashboard-v2/m/users/customer/tabs.html', locals())


def users_writer(request, pk):
    writer = User.objects.get(id=pk)
    orders = Order.objects.filter(writer=writer)
    in_progress = orders.filter(status=1)
    completed = orders.filter(status=2)
    return render(request, 'dashboard-v2/m/users/writer/tabs.html', locals())


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

    return render(request, 'dashboard-v2/m/selects/type-order.html', locals())


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

    return render(request, 'dashboard-v2/m/selects/format-order.html', locals())


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

    return render(request, 'dashboard-v2/m/selects/deadline.html', locals())


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

    return render(request, 'dashboard-v2/m/others/filter-words.html', locals())


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

    return render(request, 'dashboard-v2/m/others/testimonials.html', locals())


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

    return render(request, 'dashboard-v2/m/others/add-article.html', locals())
