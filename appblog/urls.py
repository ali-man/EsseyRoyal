from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appblog.views import ListArticles, article

app_name = 'appblog'
urlpatterns = [
    path('', ListArticles.as_view(), name='main'),
    path('<int:pk>/', article, name='article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
