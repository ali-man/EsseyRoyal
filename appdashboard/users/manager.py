from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from appdashboard.views import access_to_manager_and_admin
from apporders.forms import TypeOrderForm, FormatOrderForm, PriceDeadlineForm
from apporders.models import TypeOrder, FormatOrder, PriceDeadline, Order
from appusers.forms import UserForm, CreateUserForm
from appusers.models import User


def manager_selects(request):
    if not access_to_manager_and_admin(request.user):
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
            messages.success(request, F'{form.cleaned_data["title"]} успешно добавлен (перевести)')
            form.save()
    if '_add_format' in request.POST:
        form = FormatOrderForm(request.POST)
        if form.is_valid():
            messages.success(request, F'{form.cleaned_data["title"]} успешно добавлен (перевести)')
            form.save()
    if '_add_deadline' in request.POST:
        form = PriceDeadlineForm(request.POST)
        if form.is_valid():
            messages.success(request, F'{form.cleaned_data["title"]} успешно добавлен (перевести)')
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


def manager_users(request):
    customers = User.objects.filter(groups__name='Customer')
    orders = Order.objects.all()

    # WRITERS
    writers = User.objects.filter(groups__name='Writer')
    orders_in_progress = orders.filter(status=1)
    new_writer = CreateUserForm()

    # CUSTOMER
    customers = User.objects.filter(groups__name='Customer')

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
    return render(request, 'dashboard/manager/users/index.html', locals())


def manager_detail_writer(request, pk):
    if access_to_manager_and_admin(request.user):
        writer = User.objects.get(id=pk)
        orders = writer.order_writer.all()
        len_accepted_order = len(orders)
        in_progress = orders.filter(status=1)
        len_in_progress = len(in_progress)
        completed = orders.filter(status=2)
        len_completed = len(completed)
    else:
        messages.warning(request, 'Доступ запрещён (перевести)')
        redirect('/dashboard/')
    return render(request, 'dashboard/manager/detail/writer.html', locals())


def manager_detail_customer(request, pk):
    if access_to_manager_and_admin(request.user):
        customer = User.objects.get(id=pk)
        orders = customer.order_customer.all()
        len_orders = len(orders)
        in_progress = orders.filter(status=1)
        len_in_progress = len(in_progress)
        completed = orders.filter(status=2)
        len_completed = len(completed)
    else:
        messages.warning(request, 'Доступ запрещён (перевести)')
        redirect('/dashboard/')
    return render(request, 'dashboard/manager/detail/customer.html', locals())


# def manager_detail_writer(request, pk):
#     if access_to_manager_and_admin(request.user):
#         writer = User.objects.get(id=pk)
#         orders = writer.order_writer.all()
#         len_accepted_order = len(orders)
#         in_progress = orders.filter(status=1)
#         len_in_progress = len(in_progress)
#         completed = orders.filter(status=2)
#         len_completed = len(completed)
#     else:
#         messages.warning(request, 'Доступ запрещён (перевести)')
#         redirect('/dashboard/')
#     return render(request, 'dashboard/admin/detail/writer.html', locals())
#
#
# def manager_detail_customer(request, pk):
#     if access_to_manager_and_admin(request.user):
#         customer = User.objects.get(id=pk)
#         orders = customer.order_customer.all()
#         len_orders = len(orders)
#         in_progress = orders.filter(status=1)
#         len_in_progress = len(in_progress)
#         completed = orders.filter(status=2)
#         len_completed = len(completed)
#     else:
#         messages.warning(request, 'Доступ запрещён (перевести)')
#         redirect('/dashboard/')
#     return render(request, 'dashboard/admin/detail/customer.html', locals())