import datetime

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from apporders.forms import OrderAddForm, TypeOrderForm, FormatOrderForm, PriceDeadlineForm
from apporders.models import Order, TypeOrder, FormatOrder, PriceDeadline

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
        if user.is_superuser: # str(user_group) == '<QuerySet []>'
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
            messages.warning(self.request, 'Обнаружена ошибка, обратитесь к администрации сайта (перевести)')

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
    if request.user.is_anonymous:
        return redirect('/accounts/login/')
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
    profile_form = UserForm(instance=request.user)
    if request.method == 'POST':
        if '_change_profile' in request.POST:
            profile_form = UserForm(request.user, request.POST)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Ваш профиль успешно изменён (перевести)')
                return redirect('/dashboard/settings/')
            else:
                messages.error(request, 'Неверно заполнены поля (перевести)')
                return redirect('/dashboard/settings/')

        if '_change_password' in request.POST:
            change_password = PasswordChangeForm(user, request.POST)
            if change_password.is_valid():
                change_password.save()
                messages.success(request, 'Ваш пароль успешно изменён (перевести)')
                return redirect('/dashboard/settings/')
            else:
                messages.error(request, 'Неверно заполнены поля (перевести)')
                return redirect('/dashboard/settings/')

    return render(request, 'dashboard/admin/settings/index.html', locals())


def manager_selects(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login/')
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

    return render(request, 'dashboard/manager/selects/index.html', locals())


def manager_settings(request):
    if request.user.is_anonymous:
        return redirect('/accounts/login/')
    user = User.objects.get(email=request.user)
    change_password = PasswordChangeForm(user=user)
    profile_form = UserForm(instance=request.user)
    if request.method == 'POST':
        if '_change_profile' in request.POST:
            profile_form = UserForm(request.user, request.POST)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Ваш профиль успешно изменён (перевести)')
                return redirect('/dashboard/settings/')
            else:
                messages.error(request, 'Неверно заполнены поля (перевести)')
                return redirect('/dashboard/settings/')

        if '_change_password' in request.POST:
            change_password = PasswordChangeForm(user, request.POST)
            if change_password.is_valid():
                change_password.save()
                messages.success(request, 'Ваш пароль успешно изменён (перевести)')
                return redirect('/dashboard/settings/')
            else:
                messages.error(request, 'Неверно заполнены поля (перевести)')
                return redirect('/dashboard/settings/')

    return render(request, 'dashboard/manager/settings/index.html', locals())
