from django.contrib import admin
from django.db import models


class TypeWorks(models.Model):
    name_work = models.CharField(verbose_name='Name work', max_length=200)
    price_client = models.DecimalField(verbose_name='Цена клиента', max_digits=10, decimal_places=2)
    price_writer = models.DecimalField(verbose_name='Цена писателя', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Type work'
        verbose_name_plural = 'Types work'

    def __str__(self):
        return self.name_work


admin.site.register(TypeWorks)
