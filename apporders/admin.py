from django.contrib import admin

from apporders.models import *


class FilesOrderAdminInline(admin.TabularInline):
    model = FilesOrder
    extra = 4


class FilesAdditionallyOrderAdminInline(admin.TabularInline):
    model = FilesAdditionallyOrder
    extra = 4


class OrderAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_datetime']
    list_display_links = ['title']
    inlines = [FilesOrderAdminInline]


class AdditionallyOrderAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    list_display_links = ['__str__']
    inlines = [FilesAdditionallyOrderAdminInline]


class TypeOrderAdmin(admin.ModelAdmin):
    list_display = ['title', 'price_client', 'price_writer']
    list_display_links = ['title']


admin.site.register(PriceDeadline)
admin.site.register(FormatOrder)
admin.site.register(AdditionallyOrder, AdditionallyOrderAdmin)
admin.site.register(Chat)
admin.site.register(FeedbackOrder)
admin.site.register(FilterWord)
admin.site.register(TypeOrder, TypeOrderAdmin)
admin.site.register(Order, OrderAdmin)
