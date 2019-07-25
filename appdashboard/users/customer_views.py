import datetime

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView

from appcourses.models import Course, Task, CourseFile
from appdashboard.views import access_to_manager_and_admin
from appmail.views import manager_send_mail, writer_send_mail
from apporders.forms import OrderAddForm, OrderForm
from apporders.models import Order, FilesOrder, Chat
from apporders.validators import validate_file_views
from appusers.forms import UserCustomerForm
from appusers.models import User

check_is_customer = user_passes_test(lambda user: user.groups.all()[0].name == 'Customer' if user.is_authenticated else False)


def to_deadline(d, t):
    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute)


@check_is_customer
def index(request):
    return redirect('/c/orders/')


@check_is_customer
def orders(request):
    if request.method == 'GET':
        my_orders = Order.objects.filter(customer=request.user)
        in_review = my_orders.filter(status__in=[0, 3])
        in_process = my_orders.filter(status=1)
        completed = my_orders.filter(status=2).order_by('-completed_datetime')
        new_order = OrderAddForm()
        context = {
            'in_review': in_review,
            'in_process': in_process,
            'completed': completed,
            'new_order': new_order,
        }

        return render(request, 'dashboard-v2/c/orders/tabs.html', context=context)

    if request.method == 'POST':
        form = OrderAddForm(request.POST)
        attached_files = request.FILES.getlist('attached-files')
        if form.is_valid():
            date = form.cleaned_data['date_deadline']
            time = form.cleaned_data['time_deadline']
            deadline = to_deadline(date, time)
            order = Order()
            order.customer = user
            order.title = form.cleaned_data['title']
            order.type_order = form.cleaned_data['type_order']
            order.number_page = int(form.cleaned_data['number_page'])
            order.format_order = form.cleaned_data['format_order']
            order.deadline = deadline
            order.description = form.cleaned_data['description']
            order.save()
            if len(attached_files) != 0:
                for f in attached_files:
                    if validate_file_views(f) == 'error':
                        messages.error(request, F'{f.name} - Invalid format file')
                    else:
                        files_order = FilesOrder()
                        files_order.order = order
                        files_order.file = f
                        files_order.save()
            messages.success(request, 'Your order is loaded')
            return redirect(F'/c/orders/preview/{order.id}/')
        else:
            messages.success(request, 'The fields are incorrectly filled')
            return redirect(F'/c/orders/')


@check_is_customer
def order_preview(request, pk):
    order = get_object_or_404(Order, id=pk, status__in=[0,3], customer=request.user)
    return render(request, 'dashboard-v2/c/orders/detail/preview.html', context={'order': order})


@check_is_customer
def order_edit(request, pk):
    try:
        order = Order.objects.get(id=pk, customer=request.user)
        form = OrderForm(instance=order)
    except Order.DoesNotExist:
        messages.success(request, 'Access limited')
        return redirect('/')

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        attached_files = request.FILES.getlist('attached-files')
        if form.is_valid():
            order.title = form.cleaned_data['title']
            order.format_order = form.cleaned_data['format_order']
            order.description = form.cleaned_data['description']
            order.save()
            if len(attached_files) != 0:
                for f in attached_files:
                    if validate_file_views(f) == 'error':
                        messages.error(request, F'{f.name} - Invalid format loaded')
                    else:
                        files_order = FilesOrder()
                        files_order.order = order
                        files_order.file = f
                        files_order.save()
            messages.success(request, 'Your order is update')
            return redirect(F'/c/orders/preview/{order.id}/')
        else:
            messages.success(request, 'The fields are incorrectly filled')
            return redirect(F'/c/orders/edit/{pk}/')

    return render(request, 'dashboard-v2/c/orders/detail/edit.html', context={'form': form, 'order': order})


class UpdateOrderViews(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'dashboard-v2/c/orders/detail/edit.html'
    success_url = '/c/orders/'

    def test_func(self):
        print(self.request.user)
        obj = self.get_object()
        return obj.customer == self.request.user

    def post(self, request, *args, **kwargs):
        super(UpdateOrderViews, self).post(request, *args, **kwargs)
        if 'attached-files' in request.FILES:
            attached_files = request.FILES.getlist('attached-files')
            order = Order.objects.get(id=kwargs['pk'])
            if len(attached_files) != 0:
                for f in attached_files:
                    if validate_file_views(f) == 'error':
                        messages.error(request, F'{f.name} - Invalid format file')
                    else:
                        files_order = FilesOrder()
                        files_order.order = order
                        files_order.file = f
                        files_order.save()
        messages.success(request, 'Your order has been updated.')
        return redirect(F'/c/orders/preview/{order.id}/')


@check_is_customer
def order_in_process(request, pk):
    user = User.objects.get(email=request.user)
    if request.method == 'GET':
        order = get_object_or_404(Order, id=pk, status=1, customer=user)

        return render(request, 'dashboard-v2/c/orders/detail/in-process.html', context={'order': order})

    if request.method == 'POST':
        order = Order.objects.get(id=pk, customer=user, status=1)
        completed = request.POST.get('completed', None)

        if 'message' in request.POST and request.POST['message'] != '':
            chat = Chat()
            chat.order = order
            chat.user = user
            chat.message = request.POST['message']
            chat.status = False
            chat.save()
            manager_send_mail('New message from chat', order.customer, order.title, F'/m/orders/inprocess/{order.id}/')
            messages.success(request, 'Your message has been sent.')
            return redirect(F'/c/orders/inprocess/{pk}/')
        elif completed is not None:
            order.status = 2
            order.save()
            messages.success(request, 'Order status changed to completed')
            return redirect('/c/orders/completed/{}/'.format(pk))
        else:
            messages.success(request, 'Message cannot be empty')
            return redirect(F'/c/orders/inprocess/{pk}/')


@check_is_customer
def order_completed(request, pk):
    user = User.objects.get(email=request.user)
    order = get_object_or_404(Order, id=pk, status=2, customer=user)
    return render(request, 'dashboard-v2/c/orders/detail/completed.html', context={'order': order})


@check_is_customer
def courses(request):
    user = User.objects.get(email=request.user)
    my_course = Course.objects.filter(customer=user)
    tasks = Task.objects.exclude(status=0, course__customer=user)
    in_process = tasks.filter(status=1)
    completed = tasks.filter(status=2)
    context = {
        'my_course': my_course,
        'tasks': tasks,
        'in_process': in_process,
        'completed': completed,
    }

    if request.method == 'POST':
        title = request.POST['title']
        attached_files = request.FILES.getlist('attached-files')
        course = Course()
        course.customer = user
        course.title = title
        course.save()
        if len(attached_files) != 0:
            for f in attached_files:
                course_file = CourseFile()
                course_file.course = course
                course_file.file = f
                course_file.save()
        messages.success(request, 'Your order is loaded')
        manager_send_mail('New course', course.customer, course.title, F'/m/courses/detail/{course.id}/')
        return redirect('/c/courses/')

    return render(request, 'dashboard-v2/c/courses/tabs.html', context=context)


@check_is_customer
def settings(request):
    user = User.objects.get(email=request.user)
    user_form = UserCustomerForm(instance=user)
    change_password = PasswordChangeForm(user=user)

    if request.method == 'POST':
        r = request.POST
        _change_profile = r.get('_change_profile', None)
        _change_password = r.get('_change_password', None)
        if _change_profile is not None:
            user.first_name = r['first_name']
            user.last_name = r['last_name']
            user.academic_institution = r['academic_institution']
            user.degree = r['degree']
            user.phone = r['phone']
            if 'corporate_email' in r:
                user.corporate_email = r['corporate_email']
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            user.save()
            messages.success(request, 'Profile successfully changed')
            return redirect('/c/settings/')

        if _change_password is not None:
            change_password = PasswordChangeForm(user, request.POST)
            if change_password.is_valid():
                change_password.save()
                messages.success(request, 'Your password has been successfully changed.')
                return redirect('/c/settings/')
            else:
                messages.error(request, 'Invalid fields')
                return redirect('/c/settings/')

    return render(request, 'dashboard-v2/c/settings/tabs.html', context={
        'user_form': user_form,
        'change_password': change_password
    })


@check_is_customer
def course_detail(request, pk):
    course = Course.objects.get(id=pk)

    if request.method == 'POST':
        r = request.POST
        he_take = r.get('he_take', None)
        agree = r.get('agree', None)
        completed = r.get('completed', None)

        if he_take is not None:
            task = Task.objects.get(id=int(he_take))
            manager_send_mail(F'He take of task: {task.title}', course.customer, course.title, F'/m/courses/detail/{course.id}/')
            task.delete()

        if agree is not None:
            task = Task.objects.get(id=int(agree))
            task.price_status = 2
            task.save()
            manager_send_mail(F'Agree of task: {task.title}', course.customer, course.title, F'/m/courses/detail/{course.id}/')
            if task.to_writer:
                writer_send_mail('New task', task.title, F'/w/courses/task/{task.id}/')
        if completed is not None:
            task = Task.objects.get(id=int(completed))
            task.status = 2
            task.save()
            manager_send_mail(F'Completed task: {task.title}', course.customer, course.title, F'/m/courses/detail/{course.id}/')
            if task.to_writer:
                writer_send_mail('Completed task', task.title, F'/w/courses/task/completed/{task.id}/')

    return render(request, 'dashboard-v2/c/courses/course/course-detail.html', context={'course': course})
