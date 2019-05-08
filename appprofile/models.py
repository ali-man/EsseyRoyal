from django.conf import settings
from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    academic_institution = models.CharField(verbose_name='Academic Institution', max_length=100, blank=True)
    phone = models.CharField(verbose_name='Phone number', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def create_or_update_user_profile(sender, instance, created, **kwargs):
    #     Client.objects.get_or_create(user=instance)

    def __str__(self):
        return '%s' % self.user.get_full_name()


# class Manager(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
#     # first_name = models.CharField(verbose_name='Имя', max_length=100)
#     # second_name = models.CharField(verbose_name='Фамилия', max_length=100)
#     phone_number = models.CharField(verbose_name='Телефон номер', max_length=30)
#     corporate_email = models.EmailField(verbose_name='Корпоративный email адрес', blank=True)
#     personal_email = models.EmailField(verbose_name='Персональный email адрес')
#     photo = models.ImageField(verbose_name='Фото', upload_to='profile/photo/managers/', blank=True)
#
#     class Meta:
#         verbose_name = 'Manager'
#         verbose_name_plural = 'Managers'
#
#     @receiver(post_save, sender=settings.AUTH_USER_MODEL)
#     def create_or_update_user_profile(sender, instance, created, **kwargs):
#         Manager.objects.get_or_create(user=instance)
#
#     def __str__(self):
#         return "%s %s" % (self.user.first_name, self.user.last_name)


# class Writer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
#     # first_name = models.CharField(verbose_name='First name', max_length=50)
#     # second_name = models.CharField(verbose_name='Second name', max_length=50)
#     degree = models.CharField(verbose_name='Degree', max_length=100)
#     academic_institution = models.CharField(verbose_name='Academic Institution', max_length=100, blank=True)
#     phone_number = models.CharField(verbose_name='Телефон номер', max_length=30)
#     # works_completed = models.ManyToManyField(Order, verbose_name='Works completed', null=True, blank=True)
#     # earnings = models.ManyToManyField(Earning, verbose_name='Earnings', null=True, blank=True)
#     corporate_email = models.EmailField(verbose_name='Корпоративный email адрес', blank=True)
#     personal_email = models.EmailField(verbose_name='Персональный email адрес')
#     photo = models.ImageField(verbose_name='Фото', upload_to='profile/photo/writers/', blank=True)
#
#     class Meta:
#         verbose_name = 'Writer'
#         verbose_name_plural = 'Writers'
#
#     @receiver(post_save, sender=settings.AUTH_USER_MODEL)
#     def create_or_update_user_profile(sender, instance, created, **kwargs):
#         Writer.objects.get_or_create(user=instance)
#
#     def __str__(self):
#         return "%s %s" % (self.user.first_name, self.user.last_name)


# admin.site.register(Manager)
# admin.site.register(Client)
# admin.site.register(Writer)
