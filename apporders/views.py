import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView

from appcourses.models import Task
from appdashboard.views import access_to_manager_and_admin
from appmail.views import manager_send_mail, customer_send_mail, writer_send_mail
from apporders.forms import OrderAddForm, OrderForm
from apporders.models import Order, FilesOrder, FilesAdditionallyOrder, AdditionallyOrder, Chat, TypeOrder, FormatOrder, \
    PriceDeadline
from apporders.validators import validate_file_views
from appusers.models import User


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


class ViewOrderViews(DetailView):
    template_name = 'dashboard/customer/order/detail.html'
    model = Order
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(ViewOrderViews, self).get_context_data(**kwargs)
        return context


class UpdateOrderViews(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'dashboard/customer/order/update.html'
    success_url = '/dashboard/'

    def post(self, request, *args, **kwargs):
        super(UpdateOrderViews, self).post(request, *args, **kwargs)
        if 'attached-files' in request.FILES:
            attached_files = request.FILES.getlist('attached-files')
            order = Order.objects.get(id=kwargs['pk'])
            if len(attached_files) != 0:
                for f in attached_files:
                    if validate_file_views(f) == 'error':
                        messages.error(request, 'Invalid format loaded')
                        return redirect('/dashboard/')
                    files_order = FilesOrder()
                    files_order.order = order
                    files_order.file = f
                    files_order.save()
        messages.success(request, 'Your order has been updated.')
        return redirect('/dashboard/')


def remove_order(request):
    if '_remove' in request.POST:
        order_id = int(request.POST['_remove'])
        user = request.user
        order = Order.objects.get(id=order_id)
        if order.customer == user:
            manager_send_mail('Remove order', order.customer, order.title, '')
            order.delete()
        messages.success(request, 'Your order has been successfully deleted.')
        return redirect('/dashboard/')


def completed_order(request, pk):
    user = User.objects.get(email=request.user)
    order = Order.objects.get(id=pk, customer=user, status=1)
    order.status = 2
    order.save()
    messages.success(request, 'Order status changed to completed')
    return redirect('/order/completed/feedback/{}/'.format(pk))


def completed_order_feedback(request, pk):
    user = User.objects.get(email=request.user)
    order = Order.objects.get(id=pk, customer=user, status=2)

    return render(request, 'dashboard/customer/order/feedback.html', locals())


def add_order_views(request):
    if request.user.groups.all()[0].name == 'Customer':
        form = OrderAddForm(request.POST)
        attached_files = request.FILES.getlist('attached-files')
        if form.is_valid():
            date = form.cleaned_data['date_deadline']
            time = form.cleaned_data['time_deadline']
            deadline = to_deadline(date, time)
            order = Order()
            user = User.objects.get(email=request.user)
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


def order_published(request, pk):
    if access_to_manager_and_admin(request.user):
        order = Order.objects.get(id=pk)
        order.status = 0
        order.save()
        messages.success(request, 'Order sent to writers')
        return redirect('/dashboard/')
    else:
        messages.error(request, 'Access is denied')
        return redirect('/dashboard/')


def writer_order_completed(request, pk):
    if request.method == 'GET':
        user = User.objects.get(email=request.user)
        order = get_object_or_404(Order, id=pk, status=2, writer=user)

        return render(request, 'dashboard/writer/order/completed.html', context={'order': order})


def writer_order_detail(request, pk):
    if request.method == 'GET':
        user = User.objects.get(email=request.user)
        order = get_object_or_404(Order, id=pk, status=1, writer=user)

        return render(request, 'dashboard/writer/order/detail.html', context={'order': order})

    if request.method == 'POST':
        user = User.objects.get(email=request.user)
        order = Order.objects.get(id=pk, writer=user)
        try:
            additionally_order = AdditionallyOrder.objects.get(order=order)
        except Order.DoesNotExist:
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
            customer_send_mail('New files', order.title, order.customer.email, F'c/orders/inprocess/{order.id}/')
            manager_send_mail('New files', order.writer, order.title, F'm/orders/inprocess/{order.id}/')
            messages.success(request, 'Files uploaded successfully')
            return redirect(F'w/orders/inprocess/{order.id}/')

        if 'message' in request.POST and request.POST['message'] != '':
            chat = Chat()
            chat.order = order
            chat.user = user
            chat.message = request.POST['message']
            chat.status = False
            chat.save()

            manager_send_mail('New message from chat', order.writer, order.title, F'm/orders/inprocess/{order.id}/')
            messages.success(request, 'Your message has been sent.')
            return redirect(F'w/orders/inprocess/{order.id}/')
        else:
            messages.success(request, 'Message cannot be empty')
            return redirect(F'w/orders/inprocess/{order.id}/')


def customer_order_in_completed(request, pk):
    if request.method == 'GET':
        user = User.objects.get(email=request.user)
        order = get_object_or_404(Order, id=pk, status=2, customer=user)

        return render(request, 'dashboard/customer/order/completed.html', context={'order': order})


def customer_order_in_progress(request, pk):
    if request.method == 'GET':
        user = User.objects.get(email=request.user)
        order = get_object_or_404(Order, id=pk, status=1, customer=user)

        return render(request, 'dashboard/customer/order/progress.html', context={'order': order})

    if request.method == 'POST':
        user = User.objects.get(email=request.user)
        order = Order.objects.get(id=pk, customer=user)

        if 'message' in request.POST and request.POST['message'] != '':
            chat = Chat()
            chat.order = order
            chat.user = user
            chat.message = request.POST['message']
            chat.status = False
            chat.save()
            manager_send_mail('New message from chat', order.customer, order.title, F'm/orders/inprocess/{order.id}/')
            messages.success(request, 'Your message has been sent.')
            return redirect(F'/order/progress/{pk}/')
        else:
            messages.success(request, 'Message cannot be empty')
            return redirect(F'/order/progress/{pk}/')


def writer_order_review(request, pk):
    if request.method == 'GET':
        order = get_object_or_404(Order, id=pk, status=0)

        return render(request, 'dashboard/writer/order/review.html', context={'order': order})

    if request.method == 'POST':
        user = User.objects.get(email=request.user)
        if request.POST['take'] == 'accept':
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
            else:
                messages.warning(request, 'The order has already been accepted by another writer.')
        else:
            messages.error(request, 'Invalid request for acceptance')
        return redirect('/dashboard/')


def manager_order(request, pk):
    if request.method == 'GET':
        if not access_to_manager_and_admin(request.user):
            messages.error(request, 'Access closed')
            return redirect('/dashboard/')

        order = get_object_or_404(Order, id=pk)
        return render(request, 'dashboard/manager/orders/order/detail.html', locals())


def type_order_remove(request, pk):
    if access_to_manager_and_admin(request.user):
        type_order = TypeOrder.objects.get(id=pk)
        messages.success(request, F'{type_order.title} deleted successfully')
        type_order.delete()
    else:
        messages.error(request, 'Delete error')
        return redirect('/dashboard/')

    if request.user.is_superuser:
        return redirect('/dashboard/selects/')
    else:
        return redirect('/dashboard/m/selects/')


def format_order_remove(request, pk):
    if access_to_manager_and_admin(request.user):
        format_order = FormatOrder.objects.get(id=pk)
        messages.success(request, F'{format_order.title} deleted successfully')
        format_order.delete()
    else:
        messages.error(request, 'Delete error')
        return redirect('/dashboard/')

    if request.user.is_superuser:
        return redirect('/dashboard/selects/')
    else:
        return redirect('/dashboard/m/selects/')


def price_deadline_order_remove(request, pk):
    if access_to_manager_and_admin(request.user):
        price_deadline = PriceDeadline.objects.get(id=pk)
        messages.success(request, F'{price_deadline.price} deleted successfully')
        price_deadline.delete()
    else:
        messages.error(request, 'Delete error')
        return redirect('/dashboard/')

    if request.user.is_superuser:
        return redirect('/dashboard/selects/')
    else:
        return redirect('/dashboard/m/selects/')


def writer_tasks(request):
    writer = User.objects.get(email=request.user)
    tasks = Task.objects.filter(price_status=2, status=0, to_writer=True)
    tasks_process = Task.objects.filter(writer=writer, status=1)
    tasks_completed = Task.objects.filter(writer=writer, status=2)

    return render(request, 'dashboard/writer/tasks/index.html', locals())


def writer_task_detail(request, task_slug):
    writer = User.objects.get(email=request.user)
    task = get_object_or_404(Task, slug=task_slug, status=0)
    course = task.course
    tasks = course.task_set.filter(price_status=2, status=0)

    if request.method == 'POST':
        r = request.POST
        take = r.get('take', None)
        if take is not None:

            task_id = int(take)
            task = Task.objects.get(id=task_id, status=0)
            task.status = 1
            task.writer = writer
            task.save()

    return render(request, 'dashboard/writer/tasks/detail.html', locals())


def writer_task_process(request, task_slug):
    task = Task.objects.get(slug=task_slug)
    course = task.course

    return render(request, 'dashboard/writer/tasks/process.html', locals())
