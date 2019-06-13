from django.db import models

from appusers.models import User


class Chat(models.Model):
    owner = models.ForeignKey(User, verbose_name='Owner', related_name='massage_owner', on_delete=models.CASCADE)
    to_whom = models.ForeignKey(User, verbose_name='To whom', related_name='massage_to_whom', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(verbose_name='Message')
    created_datetime = models.DateTimeField(verbose_name='Created datetome', auto_now_add=True)

    class Meta:
        verbose_name = 'Message from chat'
        verbose_name_plural = 'Messages from chat'
        ordering = ['-id']

    def __str__(self):
        return self.message