from django.contrib import admin

from appusers.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_display_links = ['email']


admin.site.register(ChatUser)
admin.site.register(FileChatUser)
admin.site.register(MessageChatUser)
admin.site.register(User, UserAdmin)