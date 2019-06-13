from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appchat.views import main_chat

app_name = 'appchat'
urlpatterns = [
    path('', main_chat, name='main')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
