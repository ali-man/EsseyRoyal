from django.contrib import admin

from appusers.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_display_links = ['email']


class ChatUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['user']


admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(FileChatUser)
admin.site.register(MessageChatUser)
admin.site.register(User, UserAdmin)