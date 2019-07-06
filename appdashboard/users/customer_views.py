import datetime

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView

from appcourses.models import Course, Task
from appdashboard.views import access_to_manager_and_admin
from appmail.views import manager_send_mail, writer_send_mail
from apporders.forms import OrderAddForm, OrderForm
from apporders.models import Order, FilesOrder, Chat
from apporders.validators import validate_file_views
from appusers.forms import UserCustomerForm
from appusers.models import User


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


def index(request):

    return render(request, 'dashboard-v2/c/index.html', locals())


def orders(request):
    user = User.objects.get(email=request.user)

    if request.method == 'GET':
        if access_to_manager_and_admin(user):
            # TODO: Необходимо получить инфу о customer
            my_orders = Order.objects.filter(customer=user)
        elif request.user.groups.all()[0].name == 'Customer':
            my_orders = Order.objects.filter(customer=user)
        else:
            return redirect('/')
        in_review = my_orders.filter(status__in=[0, 3])
        in_process = my_orders.filter(status=1)
        completed = my_orders.filter(status=2)
        new_order = OrderAddForm()

    if request.method == 'POST':
        if request.user.groups.all()[0].name == 'Customer':
            form = OrderAddForm(request.POST)
            attached_files = request.FILES.getlist('attached-files')
            if form.is_valid():
                date = form.cleaned_data['date_deadline']
                time = form.cleaned_data['time_deadline']
                deadline = to_deadline(date, time)
                order = Order()
                order.customer = user
                order.title = form.cleaned_data['title']
                order.type_order = form.cleaned_data['type_order']
                order.number_page = form.cleaned_data['number_page']
                order.format_order = form.cleaned_data['format_order']
                order.deadline = deadline
                order.description = form.cleaned_data['description']
                order.save()
                if len(attached_files) != 0:
                    for f in attached_files:
                        if validate_file_views(f) == 'error':
                            messages.error(request, 'Invalid format loaded')
                            return redirect('/dashboard/')
                        files_order = FilesOrder()
                        files_order.order = order
                        files_order.file = f
                        files_order.save()
                messages.success(request, 'Your order is loaded')
                return redirect('/dashboard/')
            else:
                messages.success(request, 'The fields are incorrectly filled')
                return redirect('/dashboard/')
        else:
            return redirect('/')

    return render(request, 'dashboard-v2/c/orders/tabs.html', locals())


def order_preview(request, pk):
    user = User.objects.get(email=request.user)
    order = get_object_or_404(Order, id=pk, status__in=[0,3], customer=user)

    return render(request, 'dashboard-v2/c/orders/detail/preview.html', locals())


class UpdateOrderViews(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'dashboard-v2/c/orders/detail/edit.html'
    success_url = '/c/orders/'

    def post(self, request, *args, **kwargs):
        super(UpdateOrderViews, self).post(request, *args, **kwargs)
        if 'attached-files' in request.FILES:
            attached_files = request.FILES.getlist('attached-files')
            order = Order.objects.get(id=kwargs['pk'])
            if len(attached_files) != 0:
                for f in attached_files:
                    if validate_file_views(f) == 'error':
                        messages.error(request, 'Invalid format loaded')
                        return redirect('/c/orders/')
                    files_order = FilesOrder()
                    files_order.order = order
                    files_order.file = f
                    files_order.save()
        messages.success(request, 'Your order has been updated.')
        return redirect('/c/orders/')


def order_edit(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm()

    return render(request, 'dashboard-v2/c/orders/detail/edit.html', locals())


def order_in_process(request, pk):
    user = User.objects.get(email=request.user)
    if request.method == 'GET':
        order = get_object_or_404(Order, id=pk, status=1, customer=user)

        return render(request, 'dashboard-v2/c/orders/detail/in-process.html', context={'order': order})

    if request.method == 'POST':
        order = Order.objects.get(id=pk, customer=user, status=1)
        completed = request.POST.get('completed', None)

        if 'message' in request.POST and request.POST['message'] != '':
            chat = Chat()
            chat.order = order
            chat.user = user
            chat.message = request.POST['message']
            chat.status = False
            chat.save()
            manager_send_mail('New message from chat', order.customer, order.title, F'/m/orders/inprocess/{order.id}/')
            messages.success(request, 'Your message has been sent.')
            return redirect(F'/c/orders/inprocess/{pk}/')
        elif completed is not None:
            order.status = 2
            order.save()
            messages.success(request, 'Order status changed to completed')
            return redirect('/c/orders/completed/{}/'.format(pk))
        else:
            messages.success(request, 'Message cannot be empty')
            return redirect(F'/c/orders/inprocess/{pk}/')


def order_completed(request, pk):
    user = User.objects.get(email=request.user)
    order = get_object_or_404(Order, id=pk, status=2, customer=user)
    return render(request, 'dashboard-v2/c/orders/detail/completed.html', locals())


def courses(request):
    user = User.objects.get(email=request.user)
    my_course = Course.objects.filter(customer=user)
    # in_review = my_course.filter(status__in=[0, 3])
    tasks = Task.objects.exclude(status=0)
    in_process = tasks.filter(status=1)
    completed = tasks.filter(status=2)
    # new_order = OrderAddForm()

    return render(request, 'dashboard-v2/c/courses/tabs.html', locals())


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
            return redirect('/c/settings/')

        if _change_password is not None:
            change_password = PasswordChangeForm(user, request.POST)
            if change_password.is_valid():
                change_password.save()
                messages.success(request, 'Your password has been successfully changed.')
                return redirect('/c/settings/')
            else:
                messages.error(request, 'Invalid fields')
                return redirect('/c/settings/')

    return render(request, 'dashboard-v2/c/settings/tabs.html', locals())


def detail(request, pk):
    course = Course.objects.get(id=pk)

    return render(request, 'dashboard-v2/c/courses/course/detail.html', locals())
