from django import template

from appblog.models import Article
from apporders.models import Order

register = template.Library()


@register.filter(name='status_order')
def status_order(val):
    status = Order.STATUS
    return status[val][1]


@register.filter(name='len_orders')
def len_orders(customer):
    orders = customer.order_customer.all()
    return len(orders)