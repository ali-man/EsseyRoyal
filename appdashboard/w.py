from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appdashboard.users import writer_views as view

app_name = 'writer'
urlpatterns = [
    path('', view.index, name='index'),
    path('orders/preview/<int:pk>/', view.order_preview, name='order-preview'),
    path('orders/inprocess/<int:pk>/', view.order_in_process, name='order-inprocess'),
    path('orders/completed/<int:pk>/', view.order_completed, name='order-completed'),
    path('orders/', view.orders, name='orders'),
    path('courses/task/completed/<int:pk>/', view.task_completed, name='task-completed'),
    path('courses/task/inprocess/<int:pk>/', view.task_inprocess, name='task-inprocess'),
    path('courses/task/<int:pk>/', view.task_detail, name='task-detail'),
    path('courses/', view.courses, name='courses'),
    path('settings/', view.settings, name='settings'),
    path('chat/<int:pk>/', view.ChatViews.as_view(), name='chat'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
