import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView
from django.views.generic.base import View

from apporders.forms import OrderAddForm, OrderForm
from apporders.models import Order, FilesOrder, FilesAdditionallyOrder, AdditionallyOrder, Chat
from apporders.validators import validate_file_extension, validate_file_views
from appusers.models import User


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


class AddOrderViews(View):
    @staticmethod
    def get(request):
        order_form = OrderAddForm()

        return render(request, 'customer/orders/add_order.html', {'form': order_form})

    @staticmethod
    def post(request):
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
                        messages.error(request, 'Загружен не допустимый формат (перевести)')
                        return render(request, 'customer/orders/add_order.html', {'form': form})
                    files_order = FilesOrder()
                    files_order.order = order
                    files_order.file = f
                    files_order.save()
            messages.success(request, 'Ваш заказ загружен (перевести)')
            return redirect(F'/customer/order/view/{order.id}')
        else:
            messages.success(request, 'Поля не верно заполнены (перевести)')
        return render(request, 'customer/orders/add_order.html', {'form': form})


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


def remove_order(request, pk):
    user = request.user
    order = Order.objects.get(id=pk)
    if order.customer == user:
        order.remove()
    messages.success(request, 'Ваш заказ успешно удалён (перевести)')
    return redirect('/dashboard/')


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
                        messages.error(request, 'Загружен не допустимый формат (перевести)')
                        return redirect('/dashboard/')
                    files_order = FilesOrder()
                    files_order.order = order
                    files_order.file = f
                    files_order.save()
            messages.success(request, 'Ваш заказ загружен (перевести)')
            return redirect('/dashboard/')
        else:
            messages.success(request, 'Поля не верно заполнены (перевести)')
            return redirect('/dashboard/')
    else:
        return redirect('/')


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
                    messages.error(request, 'Загружен не допустимый формат (перевести)')
                    return redirect('/dashboard/')
                file_additional = FilesAdditionallyOrder()
                file_additional.additionally_order = additionally_order
                file_additional.file = f
                file_additional.save()
            messages.success(request, 'Файлы успешно загружены (перевести)')
            return redirect(F'/dashboard/w/order/detail-{pk}/')

        if 'message' in request.POST and request.POST['message'] != '':
            chat = Chat()
            chat.order = order
            chat.user = user
            chat.message = request.POST['message']
            chat.status = True
            chat.save()

            messages.success(request, 'Ваше сообщение отправлено (перевести)')
            return redirect(F'/dashboard/w/order/detail-{pk}/')
        else:
            messages.success(request, 'Сообщение не может быть пустым (перевести)')
            return redirect(F'/dashboard/w/order/detail-{pk}/')


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
            chat.status = True
            chat.save()

            messages.success(request, 'Ваше сообщение отправлено (перевести)')
            return redirect(F'/orders/progress/{pk}/')
        else:
            messages.success(request, 'Сообщение не может быть пустым (перевести)')
            return redirect(F'/orders/progress/{pk}/')


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
                messages.success(request, 'Вы успешно приняли заказ (Перевести)')
            else:
                messages.warning(request, 'Заказ уже принят другим врайтером (Перевести)')
        else:
            messages.error(request, 'Неверно отправлен запрос на принятие (Перевести)')
        return redirect('/dashboard/')
