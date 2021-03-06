from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appblog.views import ListArticles, article

app_name = 'apppayment'
urlpatterns = [
    path('ok/', ListArticles),
    path('fail/', ListArticles),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
