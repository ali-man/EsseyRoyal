from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from apporders.views import *

app_name = 'apporders'
urlpatterns = [
    path('add/', AddOrderViews.as_view(), name='add'),
    path('view/<int:pk>', ViewOrderViews.as_view(), name='view'),
    path('edit/<int:pk>', EditOrderViews.as_view(), name='edit'),
    path('remove/<int:pk>', remove_order, name='remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
