from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appdashboard.users import admin_views as view

app_name = 'administrator'
urlpatterns = [
    path('', view.index, name='index'),
    path('orders/preview/<int:pk>/', view.order_preview, name='order-preview'),
    path('orders/inprocess/<int:pk>/', view.order_in_process, name='order-inprocess'),
    path('orders/completed/<int:pk>/', view.order_completed, name='order-completed'),
    path('orders/', view.orders, name='orders'),
    path('courses/<int:pk>/', view.detail, name='course-detail'),
    path('courses/', view.courses, name='courses'),
    path('settings/', view.settings, name='settings'),
    path('users/customer/<int:pk>/', view.users_customer, name='users-customer'),
    path('users/writer/<int:pk>/', view.users_writer, name='users-writer'),
    path('users/', view.users, name='users'),
    path('type-order/', view.type_order, name='type-order'),
    path('format-order/', view.format_order, name='format-order'),
    path('deadline/', view.deadline, name='deadline'),
    path('filter-words/', view.filter_words, name='filter-words'),
    path('testimonials/', view.testimonials, name='testimonials'),
    path('add-article/', view.add_article, name='add-article'),
    path('chat/<int:pk>/', view.writer_chat, name='writer-chat'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
