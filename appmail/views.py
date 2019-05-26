from django.conf import settings
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.core.mail import send_mail


# def index(request):
#     return render(request, 'appmail/index.html')
#
#
# def success(request):
#     email = request.POST.get('email', '')
#     data = """
# Hello there!
#
# I wanted to personally write an email in order to welcome you to our platform.\
#  We have worked day and night to ensure that you get the best service. I hope \
# that you will continue to use our service. We send out a newsletter once a \
# week. Make sure that you read it. It is usually very informative.
#
# Cheers!
# ~ Yasoob
#     """
#     send_mail('Welcome!', data, "Yasoob",
#               [email], fail_silently=False)
#     return render(request, 'appmail/success.html')

# Заголовок письма, содержание письма,
# send_mail('Welcome!', data, "Yasoob", [email], fail_silently=False)


def manager_send_mail(title_mail, customer_name, order_title, link_order):
    data = '''
        Customer name: {}
        Title order: {}
        Link order: {}{}
    '''.format(customer_name, order_title, settings.LINK_DOMAIN, link_order)
    send_mail(title_mail, data, 'EssayRoyal', [settings.MANAGER_MAIL], fail_silently=False)


def customer_send_mail(title_mail, title, email, link_order):
    data = '''
        Title order: {}
        Link order: {}{}
    '''.format(title, settings.LINK_DOMAIN, link_order)
    send_mail(title_mail, data, 'EssayRoyal', email, fail_silently=False)


def writer_send_mail(title_mail, order_title, link_order):
    group = Group.objects.get(name='Writer')
    writers = []
    for w in group.user_set.all():
        writers.append(w.email)
    data = '''
            Title order: {}
            Link order: {}{}
        '''.format(order_title, settings.LINK_DOMAIN, link_order)
    send_mail(title_mail, data, 'EssayRoyal', writers, fail_silently=False)
