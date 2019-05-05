from django.shortcuts import render
from django.views.generic.base import View

from apporders.models import Order


class DashboardViews(View):
    @staticmethod
    def get(request):
        client = request.user.client
        orders = Order.objects.filter(client=client)
        works_ordered = len(orders)
        work_progress = len(orders.filter(status=1))
        complete_work = len(orders.filter(status=2))

        return render(request, 'dashboard/main.html', locals())

    @staticmethod
    def post(request):
        pass


class CustomerViews(View):
    @staticmethod
    def get(request):

        return render(request, 'dashboard/profile/customer.html', locals())

    @staticmethod
    def post(request):
        pass