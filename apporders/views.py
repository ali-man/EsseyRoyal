from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import View

from apporders.forms import OrderForm
from apporders.models import Order


class AddOrderViews(View):
    @staticmethod
    def get(request):
        order_form = OrderForm()

        return render(request, 'orders/new.html', {'form': order_form})

    @staticmethod
    def post(request):
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client = request.user.client
            instance.save()
            messages.success(request, 'Ваш заказ загружен (перевести)')
        else:
            messages.error(request, 'Не правильно заполнены поля (перевести)')

        return redirect('/')


class ViewOrderViews(DetailView):
    template_name = 'orders/view.html'
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
