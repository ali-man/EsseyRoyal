import datetime
import os

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib import admin
from django.db import models

from apporders.validators import validate_file_extension
from appusers.models import User


def upload_files(instance, filename):
    return os.path.join(settings.MEDIA_ROOT + '/customer/%s/orders/%s/attached_files/' % (
        instance.order.customer.id, instance.order.id), filename)


def writer_upload_files_to_order(instance, filename):
    customer_id = instance.additionally_order.order.customer.id
    order_id = instance.additionally_order.order.id
    path = F'/customer/{customer_id}/orders/{order_id}/writer_files/'
    result = os.path.join(settings.MEDIA_ROOT + path, filename)
    return result


class PriceDeadline(models.Model):
    days = models.IntegerField(verbose_name='Days', default=0)
    hours = models.IntegerField(verbose_name='Hours', default=0)
    price = models.DecimalField(verbose_name='Price', default=0, max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Price of deadline'
        verbose_name_plural = 'Prices of deadline'

    def save(self, *args, **kwargs):
        if self.hours == 0:
            self.hours = self.days * 24
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Days: %s / hours: %s / price: $ %s' % (self.days, self.hours, self.price)


class TypeOrder(models.Model):
    title = models.CharField(verbose_name='Type of order', max_length=50)
    price_client = models.DecimalField(verbose_name='Price for client (+ Price Deadline)', max_digits=10,
                                       decimal_places=2)
    price_writer = models.DecimalField(verbose_name='Price for writer', max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


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
    status = models.IntegerField(verbose_name='Статус', choices=STATUS, default=NOT_COMPLETED)

    class Meta:
        verbose_name = 'Earning'
        verbose_name_plural = 'Earnings'

    def save(self, *args, **kwargs):
        super(Earning, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.status


class Order(models.Model):
    IN_REVIEW = 0
    IN_PROGRESS = 1
    COMPLETED = 2

    STATUS = (
        (IN_REVIEW, 'In review'),
        (IN_PROGRESS, 'In progress'),
        (COMPLETED, 'Completed'),
    )
    customer = models.ForeignKey(User, verbose_name='Customer', related_name='order_customer', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title of order', max_length=100)
    type_order = models.ForeignKey(TypeOrder, verbose_name='Type of order', on_delete=models.CASCADE, null=True)
    format_order = models.ForeignKey(FormatOrder, verbose_name='Format of order', on_delete=models.CASCADE)
    number_page = models.IntegerField(verbose_name='Number of page', default=1)
    deadline = models.DateTimeField(verbose_name='Deadline', auto_now=False)
    description = RichTextField(verbose_name='Description')
    status = models.IntegerField(verbose_name='Status order', choices=STATUS, default=IN_REVIEW)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)
    per_page = models.DecimalField(verbose_name='Price per page', max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(verbose_name='Total cost', max_digits=10, decimal_places=2, default=0)
    writer = models.ForeignKey(User, verbose_name='Writer', related_name='order_writer', on_delete=models.CASCADE,
                               null=True, blank=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-id']

    def total_cost_writer(self):
        result = self.type_order.price_writer * self.number_page
        return result

    def save(self, *args, **kwargs):
        if self.created_datetime:
            deadline = (self.deadline - self.created_datetime).total_seconds()
            print('create_datetime')
        else:
            deadline = (self.deadline - datetime.datetime.now()).total_seconds()
            print('today')
        hours = int(divmod(deadline, 3600)[0])
        print(hours)
        deadlines_price = PriceDeadline.objects.filter(hours__lte=hours)
        print(deadlines_price)
        last_index = len(deadlines_price) - 1  # Последний индекс из queryset
        price = deadlines_price[last_index].price + self.type_order.price_client  # Цена type of order
        self.per_page = price
        self.total_cost = price * self.number_page

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class FilesOrder(models.Model):
    # TODO: Загрузка файлов не более 10, и форматов .xls .doc .docx .pdf .jpg .png .excel
    order = models.ForeignKey(Order, verbose_name='ID Order', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Attached files', upload_to=upload_files, validators=[validate_file_extension],
                            null=True, blank=True)

    def __str__(self):
        return '%s' % self.id


class AdditionallyOrder(models.Model):
    order = models.OneToOneField(Order, verbose_name='Order', on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)
    updated_datetime = models.DateTimeField(verbose_name='Updated datetime', auto_now=True)

    class Meta:
        verbose_name = 'Additionally order'
        verbose_name_plural = 'Additionally orders'

    def __str__(self):
        return '%s' % self.order


class FilesAdditionallyOrder(models.Model):
    additionally_order = models.ForeignKey(AdditionallyOrder, verbose_name='Additionally order',
                                           on_delete=models.CASCADE)
    file = models.FileField(verbose_name='File', upload_to=writer_upload_files_to_order)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'File additionally order'
        verbose_name_plural = 'Files additionally order'

    def __str__(self):
        return '%s' % self.file.url


class Chat(models.Model):
    order = models.ForeignKey(Order, verbose_name='Order', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Message')
    status = models.BooleanField(verbose_name='Send', default=False)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return self.message
