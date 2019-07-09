from django.db import models

from appusers.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(verbose_name='Fullname', max_length=50, blank=True)
    academic_institution = models.CharField(verbose_name='Academic Institution', max_length=100, blank=True)
    comment = models.TextField(verbose_name='Comment')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.comment


class Feedback(models.Model):
    name = models.CharField(verbose_name='Your name', max_length=50)
    email = models.EmailField(verbose_name='Email', max_length=50)
    subject = models.CharField(verbose_name='Subject', max_length=100)
    message = models.TextField(verbose_name='Message')

    ip = models.CharField(verbose_name='IP address', max_length=50, blank=True)
    country = models.CharField(verbose_name='Country', max_length=100, blank=True)
    city = models.CharField(verbose_name='City', max_length=100, blank=True)
    time_zone = models.CharField(verbose_name='Time zone', max_length=100, blank=True)

    device = models.CharField(verbose_name='Device', max_length=50, blank=True)
    browser = models.CharField(verbose_name='Browser', max_length=100, blank=True)
    operation_system = models.CharField(verbose_name='OS', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = "Feedback's"

    def __str__(self):
        return self.name
