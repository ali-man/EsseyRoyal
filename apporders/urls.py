from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from apporders.views import *

app_name = 'apporders'
urlpatterns = [
    path('progress/<int:pk>/', customer_order_in_progress, name='customer-progress_order'),
    path('completed/<int:pk>/', customer_order_in_completed, name='customer-completed_order'),
    path('view/<int:pk>/', ViewOrderViews.as_view(), name='view_order'),
    path('update/<int:pk>/', UpdateOrderViews.as_view(), name='update_order'),
    path('new', add_order_views, name='add_order'),
    path('remove', remove_order, name='remove'),
    path('completed/<int:pk>/', completed_order, name='completed'),
    path('completed/feedback/<int:pk>/', completed_order_feedback, name='completed-feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
