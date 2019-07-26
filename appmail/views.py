from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail


def for_get_mail_from_managers():
    group = Group.objects.get(name='Manager')
    managers = []
    for m in group.user_set.all():
        if m.corporate_email:
            managers.append(m.corporate_email)

    return managers


def manager_rest_of_time_send_mail(title_mail, order_title, order_link):
    data = '''
        Title: {}
        Link: {}dashboard/m/order/{}/
    '''.format(order_title, settings.LINK_DOMAIN, order_link)
    emails = for_get_mail_from_managers()
    send_mail(title_mail, data, 'EssayRoyal', emails, fail_silently=False)


def writer_rest_of_time_send_mail(title_mail, order_title, order_link, email):
    data = '''
        Title: {}
        Link: {}dashboard/w/order/detail-{}/
    '''.format(order_title, settings.LINK_DOMAIN, order_link)
    send_mail(title_mail, data, 'EssayRoyal', [email], fail_silently=False)


def manager_send_mail(title_mail, customer_name, order_title, link_order):
    managers = for_get_mail_from_managers()
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


def manager_send_mail_of_feedback(info):
    managers = for_get_mail_from_managers()
    data = F'''
            Name: {info['name']} 
            Email: {info['email']}
            Subject: {info['subject']}
            Message: {info['message']}
            IP: {info['ip']}
            Country: {info['country']}
            City: {info['city']}
            Timezone: {info['time_zone']}
            Device: {info['device']}
            Browser: {info['browser']}
            Operation system {info['os']}
        '''

    send_mail('New feedback', data, 'EssayRoyal', managers, fail_silently=False)


def notification_to_writer(link, writer_mail):
    data = F'''
            New messages in chat!
            Link: {settings.LINK_DOMAIN}{link}
        '''
    send_mail('New messages in chat', data, 'EssayRoyal', [writer_mail], fail_silently=False)


def notification_to_managers(link):
    managers = for_get_mail_from_managers()
    data = F'''
            New messages in chat!
            Link: {settings.LINK_DOMAIN}{link}
        '''
    send_mail('New messages in chat', data, 'EssayRoyal', managers, fail_silently=False)
