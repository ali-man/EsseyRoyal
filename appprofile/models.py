from django.db import models
from django.contrib import admin


class Manager(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=100)
    second_name = models.CharField(verbose_name='Фамилия', max_length=100)
    phone_number = models.CharField(verbose_name='Телефон номер', max_length=30)
    corporate_email = models.EmailField(verbose_name='Корпоративный email адрес', blank=True)
    personal_email = models.EmailField(verbose_name='Персональный email адрес')
    photo = models.ImageField(verbose_name='Фото', upload_to='profile/photo/managers/', blank=True)

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'

    def __str__(self):
        return "%s %s" % (self.second_name, self.first_name)


class Client(models.Model):
    first_name = models.CharField(verbose_name='First name', max_length=50)
    second_name = models.CharField(verbose_name='Second name', max_length=50)
    academic_institution = models.CharField(verbose_name='Academic Institution', max_length=100, blank=True)
    phone = models.CharField(verbose_name='Phone number', max_length=50)
    # orders = models.ManyToManyField(Order, verbose_name='Orders', null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=100)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return "%s %s" % (self.second_name, self.first_name)


class Writer(models.Model):
    first_name = models.CharField(verbose_name='First name', max_length=50)
    second_name = models.CharField(verbose_name='Second name', max_length=50)
    degree = models.CharField(verbose_name='Degree', max_length=100)
    academic_institution = models.CharField(verbose_name='Academic Institution', max_length=100, blank=True)
    phone_number = models.CharField(verbose_name='Телефон номер', max_length=30)
    # works_completed = models.ManyToManyField(Order, verbose_name='Works completed', null=True, blank=True)
    # earnings = models.ManyToManyField(Earning, verbose_name='Earnings', null=True, blank=True)
    corporate_email = models.EmailField(verbose_name='Корпоративный email адрес', blank=True)
    personal_email = models.EmailField(verbose_name='Персональный email адрес')
    photo = models.ImageField(verbose_name='Фото', upload_to='profile/photo/writers/', blank=True)

    class Meta:
        verbose_name = 'Writer'
        verbose_name_plural = 'Writers'

    def __str__(self):
        return "%s %s" % (self.second_name, self.first_name)


admin.site.register(Manager)
admin.site.register(Client)
admin.site.register(Writer)