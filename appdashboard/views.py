from django.shortcuts import render, redirect
from django.views.generic.base import View

from apporders.models import Order, TypeOrder, FormatOrder
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
        types_order = TypeOrder.objects.all()
        formats_order = FormatOrder.objects.all()
        if not request.user.is_superuser:
            return redirect('/')

        return render(request, 'admin/admin-dashboard.html', locals())

    @staticmethod
    def post(request):
        print(
            request.POST
        )
        if 'type_order' in request.POST:
            type_order = TypeOrder(
                title=request.POST['type_order']
            )
            type_order.save()

        if 'type_order_remove' in request.POST:
            id = request.POST['type_order_remove']
            type_order = TypeOrder.objects.get(id=int(id))
            type_order.delete()

        if 'format_order' in request.POST:
            format_order = FormatOrder(
                title=request.POST['format_order']
            )
            format_order.save()

        if 'format_order_remove' in request.POST:
            id = request.POST['format_order_remove']
            format_order = FormatOrder.objects.get(id=int(id))
            format_order.delete()

        # if 'academic_level' in request.POST:
        #     academic_level = AcademicLevel(
        #         title=request.POST['academic_level']
        #     )
        #     academic_level.save()
        #
        # if 'academic_level_remove' in request.POST:
        #     id = request.POST['academic_level_remove']
        #     academic_level = AcademicLevel.objects.get(id=int(id))
        #     academic_level.delete()

        return redirect('/admin')


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