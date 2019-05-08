from django.shortcuts import render, redirect
from django.views.generic.base import View

from apporders.models import Order
from appusers.models import User


def dashboard_redirect(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin')
    elif user.is_client:
        return redirect('/customer')
    elif user.is_manager:
        return redirect('/manager')
    elif user.is_writer:
        return redirect('/writer')
    else:
        return redirect('/')


class CustomerDashboardViews(View):
    @staticmethod
    def get(request):
        if request.user.is_anonymous:
            return redirect('/')
        user = User.objects.get(id=request.user.id)
        client = user.client
        orders = client.order_set.all()
        works_ordered = len(orders)
        work_progress = len(orders.filter(status=1))
        complete_work = len(orders.filter(status=2))

        return render(request, 'customer/customer-dashboard.html', locals())


class AdminDashboardViews(View):
    @staticmethod
    def get(request):
        if not request.user.is_superuser:
            return redirect('/')

        return render(request, 'admin/admin-dashboard.html', locals())


class WritersAdminDashboardViews(View):
    @staticmethod
    def get(request):

        return render(request, 'admin/writers-admin-dashboard.html', locals())


class OrderReviewAdminDashboardViews(View):
    @staticmethod
    def get(request):
        orders = Order.objects.all()
        return render(request, 'admin/order_review-admin-dashboard.html', context={'orders': orders})


class OrderAdminDashboardViews(View):
    @staticmethod
    def get(request):
        orders = Order.objects.all()
        return render(request, 'admin/orders-admin-dashboard.html', context={'orders': orders})