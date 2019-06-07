from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail


def manager_send_mail(title_mail, customer_name, order_title, link_order):
    group = Group.objects.get(name='Manager')
    managers = []
    for m in group.user_set.all():
        if m.corporate_email:
            managers.append(m.corporate_email)
    data = '''
        Name: {}
        Title: {}
        Link: {}{}
    '''.format(customer_name, order_title, settings.LINK_DOMAIN, link_order)
    send_mail(title_mail, data, 'EssayRoyal', managers, fail_silently=False)


def customer_send_mail(title_mail, title, email, link_order):
    data = '''
        Title order: {}
        Link order: {}{}
    '''.format(title, settings.LINK_DOMAIN, link_order)
    send_mail(title_mail, data, 'EssayRoyal', [email], fail_silently=False)


def writer_send_mail(title_mail, order_title, link_order, email=None):
    group = Group.objects.get(name='Writer')
    if email is None:
        writers = []
        for w in group.user_set.all():
            writers.append(w.email)
    else:
        writers = [email]
    data = '''
            Title order: {}
            Link order: {}{}
        '''.format(order_title, settings.LINK_DOMAIN, link_order)
    send_mail(title_mail, data, 'EssayRoyal', writers, fail_silently=False)
