import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views.generic.base import View, TemplateView

from appdashboard.mixins import DashBoardMixin, EditProfileMixin
from apporders.forms import OrderAddForm, TypeOrderForm, FormatOrderForm, PriceDeadlineForm
from apporders.models import Order, TypeOrder, FormatOrder, PriceDeadline, FilesOrder
from apporders.validators import validate_file_views
from appusers.forms import UserForm, CreateUserForm
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


class ManagerDashboardViews(View):

    @staticmethod
    def get(request):
        if request.user.is_anonymous:
            return redirect('/')
        user = User.objects.get(id=request.user.id)
        orders = Order.objects.all()
        order_moderation = orders.filter(send_writer=False)

        return render(request, 'manager/manager-dashboard.html', context={
            'user': user,
            'orders_moderation': order_moderation,
            'orders': orders
        })


class AdminDashboardViews(View):
    @staticmethod
    def get(request):
        types_order = TypeOrder.objects.all()
        formats_order = FormatOrder.objects.all()
        price_deadline = PriceDeadline.objects.all()
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
                title=request.POST['title'],
                price_writer=request.POST['price_for_writer'],
                price_client=request.POST['price_for_client']
            )
            type_order.save()

        if 'type_order_remove' in request.POST:
            id = request.POST['type_order_remove']
            type_order = TypeOrder.objects.get(id=int(id))
            type_order.delete()

        if 'format_order' in request.POST:
            format_order = FormatOrder(
                title=request.POST['title']
            )
            format_order.save()

        if 'format_order_remove' in request.POST:
            id = request.POST['format_order_remove']
            format_order = FormatOrder.objects.get(id=int(id))
            format_order.delete()

        if 'price_deadline' in request.POST:
            price_deadline = PriceDeadline(
                start_day=request.POST['start_day'],
                end_day=request.POST['end_day'],
                price=request.POST['price']
            )
            price_deadline.save()

        if 'price_deadline_remove' in request.POST:
            id = request.POST['price_deadline_remove']
            price_deadline = PriceDeadline.objects.get(id=int(id))
            price_deadline.delete()

        return redirect('/admin')


class WritersAdminDashboardViews(View):
    @staticmethod
    def get(request):
        # writers = Writer.objects.all()

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
                create_user.phone = phone
                create_user.corporate_email = corporate_email
                create_user
                create_user.save()
            else:
                messages.error(request, 'Пароли не совпадают (перевести)')

            return redirect('/admin/writers/')


class ManagersAdminDashboardViews(View):
    @staticmethod
    def get(request):
        # managers = Manager.objects.all()
        return render(request, 'admin/managers-admin-dashboard.html', locals())

    @staticmethod
    def post(request):
        if 'create_manager' in request.POST:
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
                create_user.is_manager = True
                create_user.phone = phone
                create_user.corporate_email = corporate_email
                create_user.save()
            else:
                messages.error(request, 'Пароли не совпадают (перевести)')

            return redirect('/admin/managers/')


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


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


class DashboardViews(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_group = user.groups.all()
        groups = Group.objects.all()
        customer = groups.get(name='Customer')
        writer = groups.get(name='Writer')
        manager = groups.get(name='Manager')
        orders = Order.objects.all()
        context['user_form'] = UserForm(instance=user)

        # ADMIN
        if str(user_group) == '<QuerySet []>':
            context['profile'] = 'admin'
            # Orders
            context['orders'] = orders
            context['orders_in_review'] = orders.filter(status=0)
            context['orders_in_progress'] = orders.filter(status=1)
            context['orders_completed'] = orders.filter(status=2)
            # Users
            context['customers'] = customer.user_set.all()
            context['writers'] = writer.user_set.all()
            context['managers'] = manager.user_set.all()

        # CUSTOMER
        elif user_group[0] == customer:
            context['profile'] = 'customer'
            context['orders'] = user.order_customer.all()
            context['new_order'] = OrderAddForm()

        # WRITER
        elif user_group[0] == writer:
            context['profile'] = 'writer'
            context['orders_in_review'] = orders.filter(status=0)
            context['orders_in_progress'] = user.order_writer.filter(status=1)
            context['orders_completed'] = user.order_writer.filter(status=2)

        # MANAGER
        elif user_group[0] == manager:
            context['profile'] = 'manager'
            # Orders
            context['orders'] = orders
            context['orders_in_review'] = orders.filter(status=0)
            context['orders_in_progress'] = orders.filter(status=1)
            context['orders_completed'] = orders.filter(status=2)
            # Users
            context['customers'] = customer.user_set.all()
            context['writers'] = writer.user_set.all()
            context['manager'] = manager.user_set.all()

        # NOT GROUP
        else:
            print('Вы не состоите не в одной группе или не авторизованы')

        return context


# ADMIN

def admin_users(request):
    customers = User.objects.filter(groups__name='Customer')
    orders = Order.objects.all()

    # WRITERS
    writers = User.objects.filter(groups__name='Writer')
    orders_in_progress = orders.filter(status=1)
    new_writer = CreateUserForm()

    # CUSTOMER
    customers = User.objects.filter(groups__name='Customer')

    # Managers
    managers = User.objects.filter(groups__name='Manager')
    new_manager = CreateUserForm()


    if request.method == 'POST':
        if '_create_writer' in request.POST:
            form_writer = CreateUserForm(request.POST, request.FILES)
            if form_writer.is_valid():
                cd = form_writer.cleaned_data
                g = Group.objects.get(name='Writer')
                user = User()
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.email = cd['email']
                user.set_password(cd['password'])
                user.corporate_email = cd['corporate_email']
                user.phone = cd['phone']
                user.academic_institution = cd['academic_institution']
                user.degree = cd['degree']
                user.avatar = cd['avatar']
                user.save()
                user.groups.add(g)
                user.save()
                messages.success(request, 'Новый врайтер успешно создан (певести)')
            else:
                messages.error(request, 'Неверно заполнены поля (певести)')

        if '_create_manager' in request.POST:
            create_manager = CreateUserForm(request.POST, request.FILES)
            if create_manager.is_valid():
                cd = create_manager.cleaned_data
                g = Group.objects.get(name='Manager')
                user = User()
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.email = cd['email']
                user.set_password(cd['password'])
                user.corporate_email = cd['corporate_email']
                user.phone = cd['phone']
                user.academic_institution = cd['academic_institution']
                user.degree = cd['degree']
                user.avatar = cd['avatar']
                user.save()
                user.groups.add(g)
                user.save()
                messages.success(request, 'Новый manager успешно создан (певести)')
            else:
                messages.error(request, 'Неверно заполнены поля (певести)')

    return render(request, 'dashboard/admin/users/index.html', locals())


def admin_selects(request):
    types = TypeOrder.objects.all()
    formats = FormatOrder.objects.all()
    deadlines = PriceDeadline.objects.all()

    type_form = TypeOrderForm()
    format_form = FormatOrderForm()
    deadline_form = PriceDeadlineForm()

    if '_add_type' in request.POST:
        form = TypeOrderForm(request.POST)
        if form.is_valid():
            form.save()
    if '_add_format' in request.POST:
        form = FormatOrderForm(request.POST)
        if form.is_valid():
            form.save()
    if '_add_deadline' in request.POST:
        form = PriceDeadlineForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'dashboard/admin/selects/index.html', locals())


def admin_settings(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login/')
    user = User.objects.get(email=request.user)
    change_password = PasswordChangeForm(user=user)
    if request.method == 'POST':
        change_password = PasswordChangeForm(user, request.POST)
        if change_password.is_valid():
            change_password.save()
            messages.success(request, 'Ваш пароль успешно изменён (перевести)')
            return redirect('/dashboard/settings/')
        else:
            messages.error(request, 'Неверно заполнены поля (перевести)')
            return redirect('/dashboard/settings/')

    return render(request, 'dashboard/admin/settings/index.html', locals())
