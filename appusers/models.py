from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', unique=True)
    first_name = models.CharField(verbose_name='Name', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='surname', max_length=30, blank=True)
    date_joined = models.DateTimeField(verbose_name='registered', auto_now_add=True)
    is_staff = models.BooleanField(verbose_name='is_staff', default=False)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    phone = models.CharField(verbose_name='Phone number', max_length=50, blank=True)
    academic_institution = models.CharField(verbose_name='Academic Institution', max_length=100, blank=True)
    corporate_email = models.EmailField(verbose_name='Corporate email', blank=True)
    degree = models.CharField(verbose_name='Degree', max_length=100, blank=True)

    balance = models.DecimalField(verbose_name='Balance', max_digits=10, decimal_places=2, default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        '''
        Возвращает first_name и last_name с пробелом между ними.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name) if self.first_name and self.last_name is not '' else self.email
        return full_name.strip()

    def get_short_name(self):
        '''
        Возвращает сокращенное имя пользователя.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Отправляет электронное письмо этому пользователю.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)