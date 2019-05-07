from django.shortcuts import render
from django.views.generic.base import View

from apporders.models import Order
from appusers.models import User


class CustomerDashboardViews(View):
    @staticmethod
    def get(request):
        user = User.objects.get(id=request.user.id)
        client = user.client
        orders = client.order_set.all()
        works_ordered = len(orders)
        work_progress = len(orders.filter(status=1))
        complete_work = len(orders.filter(status=2))

        return render(request, 'customer/dashboard.html', locals())


class AdminDashboardViews(View):
    @staticmethod
    def get(request):

        return render(request, 'admin/dashboard.html', locals())