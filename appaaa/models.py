from django.db import models

from appusers.models import User


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
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

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = "Feedback's"

    def __str__(self):
        return self.name
