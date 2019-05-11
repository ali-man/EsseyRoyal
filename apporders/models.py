import os

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib import admin
from django.db import models

from apporders.validators import validate_file_extension
from appprofile.models import Client


def upload_files(instance, filename):
    return os.path.join(settings.MEDIA_ROOT + '/customer/%s/orders/%s/attached_files/' % (instance.order.client.id, instance.order.id), filename)


class TypeOrder(models.Model):
    title = models.CharField(verbose_name='Type of order', max_length=50)

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
    # client = models.ForeignKey('Client', verbose_name='Клиент', on_delete=models.CASCADE)
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
    client = models.ForeignKey(Client, verbose_name='Client', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title of order', max_length=100)
    type_order = models.ForeignKey(TypeOrder, verbose_name='Type of order', on_delete=models.CASCADE, null=True)
    format_order = models.ForeignKey(FormatOrder, verbose_name='Format of order', on_delete=models.CASCADE)
    deadline = models.DateTimeField(verbose_name='Deadline', auto_now=False)
    description = RichTextField(verbose_name='Description')
    status = models.IntegerField(verbose_name='Status order', choices=STATUS, default=IN_REVIEW)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.title


class FilesOrder(models.Model):
    # TODO: Загрузка файлов не более 10, и форматов .xls .doc .docx .pdf .jpg .png .excel
    order = models.ForeignKey(Order, verbose_name='ID Order', on_delete=models.CASCADE)
    file = models.FileField(verbose_name='Attached files', upload_to=upload_files, validators=[validate_file_extension], null=True, blank=True)

    def __str__(self):
        return '%s' % self.id
