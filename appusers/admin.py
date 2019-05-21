from django.contrib import admin

from appusers.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_display_links = ['email']


admin.site.register(User, UserAdmin)