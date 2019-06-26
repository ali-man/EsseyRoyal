from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appcourses.views import course_index

app_name = 'appcourses'
urlpatterns = [
    path('', course_index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
