import datetime

from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from appaaa.models import Feedback, Comment
from appblog.forms import ArticleForm
from apporders.forms import OrderAddForm
from apporders.models import Order, FilterWord

from appusers.forms import UserForm, UserCustomerForm
from appusers.models import User


def access_to_manager_and_admin(_user):
    is_access = False
    if _user.is_authenticated:
        user = User.objects.get(email=_user)
        if user.is_superuser:
            is_access = True
        for g in user.groups.all():
            if g.name == 'Manager':
                is_access = True
    return is_access


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
            context['orders_in_review'] = orders.filter(status__in=[0, 3])
            context['orders_in_progress'] = orders.filter(status=1)
            context['orders_completed'] = orders.filter(status=2)
            # Users
            context['customers'] = customer.user_set.all()
            context['writers'] = writer.user_set.all()
            context['managers'] = manager.user_set.all()

        # CUSTOMER
        elif user_group[0] == customer:
            context['user_form'] = UserCustomerForm(instance=user)
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
            context['orders_in_review'] = orders.filter(status__in=[0, 3])
            context['orders_in_progress'] = orders.filter(status=1)
            context['orders_completed'] = orders.filter(status=2)
            # Users
            context['customers'] = customer.user_set.all()
            context['writers'] = writer.user_set.all()
            context['manager'] = manager.user_set.all()

        # NOT GROUP
        else:
            messages.warning(self.request, 'An error was found, contact the site administration.')

        return context


def others(request):
    if not access_to_manager_and_admin(request.user):
        messages.error(request, 'Access closed')
        return redirect('/dashboard/')
    context = {}
    # Filter word
    context['words'] = FilterWord.objects.all()
    # Comments
    context['comments'] = Comment.objects.all()
    # Add article
    context['form'] = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article successfully added')
            return redirect('/dashboard/others/')
        else:
            context['form'] = ArticleForm(request.POST, request.FILES)
            messages.error(request, 'Invalid fields')

    return render(request, 'dashboard/others/index.html', context=context)


# def feedback_view(request, pk):
#     if not access_to_manager_and_admin(request.user):
#         messages.error(request, 'Access closed')
#         return redirect('/dashboard/')
#     feedback = Feedback.objects.get(id=pk)
#     return render(request, 'dashboard/others/detail/feedback.html', {'feedback': feedback})


def comment_view(request, pk):
    if not access_to_manager_and_admin(request.user):
        messages.error(request, 'Access closed')
        return redirect('/dashboard/')
    comment = Comment.objects.get(id=pk)
    return render(request, 'dashboard/others/detail/comment.html', {'comment': comment})
