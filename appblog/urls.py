from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appblog.views import ListArticles

app_name = 'appblog'
urlpatterns = [
    path('', ListArticles.as_view(), name='main'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
