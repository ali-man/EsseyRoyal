from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appblog.views import ListArticles, article, article_edit, article_remove

app_name = 'appblog'
urlpatterns = [
    path('', ListArticles.as_view(), name='main'),
    path('article/<int:pk>/edit/', article_edit, name='article-edit'),
    path('article/<int:pk>/remove/', article_remove, name='article-remove'),
    path('article/<int:pk>/', article, name='article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
