from django.contrib import admin
from appcourses.models import *


admin.site.register(Course)
admin.site.register(CourseFile)
admin.site.register(Task)
admin.site.register(TaskFile)