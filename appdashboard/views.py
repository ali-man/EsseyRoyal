from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.base import View

from apporders.models import Order, TypeOrder, FormatOrder
from appprofile.forms import WriterForm
from appprofile.models import Writer, Client
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
        writers = Writer.objects.all()

        return render(request, 'admin/writers-admin-dashboard.html', locals())

    @staticmethod
    def post(request):
        if 'create_writer' in request.POST:
            r = request.POST
            first_name = r['firstname']
            last_name = r['lastname']
            email = r['email']
            corporate_email = r['corporate-email']
            phone = r['phone']
            password1 = r['password1']
            password2 = r['password2']
            if password1 == password2:
                create_user = User.objects.create_user(email=email, password=password2)
                create_user.first_name = first_name
                create_user.last_name = last_name
                create_user.is_writer = True
                create_user.save()
                writer = Writer()
                writer.phone_number = phone
                writer.corporate_email = corporate_email
                writer.user = create_user
                writer.save()
            else:
                messages.error(request, 'Пароли не совпадают (перевести)')

            return redirect('/admin/writers/')


class EditWriterAdminDashboardViews(View):
    @staticmethod
    def get(request, pk):
        writer = Writer.objects.get(id=pk)
        form = WriterForm(instance=writer)
        return render(request, 'admin/writer-edit-admin-dashboard.html', context={'form': form, 'writer': writer})

    @staticmethod
    def post(request, pk):
        writer = Writer.objects.get(id=pk)
        form = WriterForm(request.POST, request.FILES, instance=writer)
        print(request.FILES)
        if form.is_valid():
            if 'photo' in request.FILES:
                form.photo = request.FILES['photo']
            form.save()
            messages.success(request, 'Врайтер успешно изменён (перевести)')
            return redirect('/admin/writers/')
        else:
            return render(request, 'admin/writer-edit-admin-dashboard.html', context={'form': form, 'writer': writer})


class ClientsAdminDashboardViews(View):
    @staticmethod
    def get(request):
        clients = Client.objects.all()

        return render(request, 'admin/clients-admin-dashboard.html', locals())


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