import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.base import View

from apporders.forms import OrderAddForm
from apporders.models import Order, FilesOrder
from apporders.validators import validate_file_extension, validate_file_views


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
            order.client = request.user.client
            order.title = form.cleaned_data['title']
            order.type_order = form.cleaned_data['type_order']
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
    template_name = 'customer/orders/view_order.html'
    model = Order
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(ViewOrderViews, self).get_context_data(**kwargs)
        return context


class EditOrderViews(View):
    pass


def remove_order(request, pk):
    client = request.user.client
    order = Order.objects.get(id=pk)
    if order.client == client:
        order.remove()
    messages.success(request, 'Ваш заказ успешно удалён (перевести)')
    return redirect('/')
