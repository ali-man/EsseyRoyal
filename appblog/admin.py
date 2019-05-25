from django.contrib import admin

from appblog.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']


admin.site.register(Article, ArticleAdmin)