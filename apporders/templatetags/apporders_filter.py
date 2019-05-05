from django import template

from apporders.models import Order

register = template.Library()


@register.filter(name='status_order')
def status_order(val):
    status = Order.STATUS
    return status[val][1]