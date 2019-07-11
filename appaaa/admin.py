from django.contrib import admin
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from appaaa.models import Feedback, Comment


# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


# Re-register FlatPageAdmin

class AdminComment(admin.ModelAdmin):
    list_display = ['comment', 'checked']
    list_display_links = ['comment']
    list_editable = ['checked']


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Feedback)
admin.site.register(Comment, AdminComment)
