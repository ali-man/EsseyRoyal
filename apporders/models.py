from django.contrib import admin
from django.db import models

from appprofile.models import Client, Manager, Writer


class FormatOrder(models.Model):
    title = models.CharField(verbose_name='Format of order', max_length=50)

    class Meta:
        verbose_name = 'Format of order'
        verbose_name_plural = 'Format of orders'

    def __str__(self):
        return self.title


class Earning(models.Model):
    NOT_COMPLETED = 0
    COMPLETED = 1
    STATUS = (
        (NOT_COMPLETED, 'Not completed'),
        (COMPLETED, 'Completed')
    )

    date_order = models.DateTimeField(verbose_name='Дата получения заказа', auto_now_add=True)
    number_pages = models.IntegerField(verbose_name='Количество страниц', default=0)
    earned_amount = models.DecimalField(verbose_name='Цена клиента', max_digits=10, decimal_places=2)
    # client = models.ForeignKey('Client', verbose_name='Клиент', on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='Статус', choices=STATUS, default=NOT_COMPLETED)

    class Meta:
        verbose_name = 'Earning'
        verbose_name_plural = 'Earnings'

    def save(self, *args, **kwargs):
        super(Earning, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.status


class DeadLine(models.Model):
    date_deadline = models.CharField(verbose_name='DeadLine', max_length=100)

    class Meta:
        verbose_name = 'Deadline'
        verbose_name_plural = 'Deadlines'

    def __str__(self):
        return self.date_deadline


class Order(models.Model):
    title = models.CharField(verbose_name='Title of order', max_length=100)
    type_order = models.CharField(verbose_name='Type of order', max_length=100)
    format_order = models.ForeignKey(FormatOrder, verbose_name='Format of order', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name='Client', on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, verbose_name='Responsible manager', on_delete=models.CASCADE, null=True)
    writer = models.ForeignKey(Writer, verbose_name='Responsible writer', on_delete=models.CASCADE, null=True)
    deadline = models.ForeignKey(DeadLine, verbose_name='Deadline', on_delete=models.CASCADE)
    deadline_writer = models.DateTimeField(verbose_name='Deadline by writer')
    feedback = models.TextField(verbose_name='Feedback')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.title


admin.site.register(FormatOrder)
admin.site.register(Earning)
admin.site.register(DeadLine)
admin.site.register(Order)