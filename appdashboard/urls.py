from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appdashboard.users.admin import *
from appdashboard.users.manager import *
from appdashboard.views import *
from apporders.views import *
from appusers.views import change_profile

app_name = 'appdashboard'
urlpatterns = [
    path('change-profile/', change_profile, name='change-profile'),
    # WRITER
    path('w/order/completed-<int:pk>/', writer_order_completed, name='writer-order_completed'),
    path('w/order/detail-<int:pk>/', writer_order_detail, name='writer-order_detail'),
    path('w/order/review-<int:pk>/', writer_order_review, name='writer-order_review'),
    # path('feedback/<int:pk>/', feedback_view, name='feedback-view'),
    path('others/comment/<int:pk>/', comment_view, name='comment-view'),
    path('others/', others, name='others'),
    # ADMIN
    path('writer/<int:pk>/', admin_detail_writer, name='admin-writer'),
    path('customer/<int:pk>/', admin_detail_customer, name='admin-customer'),
    path('manager/<int:pk>/', admin_detail_manager, name='admin-manager'),
    path('users/', admin_users, name='admin-users'),
    path('selects/', admin_selects, name='admin-selects'),
    path('settings/', admin_settings, name='admin-settings'),
    path('billing/', DashboardViews.as_view(), name='admin-billing'),
    # Manager
    path('m/writer/<int:pk>/', manager_detail_writer, name='manager-writer'),
    path('m/customer/<int:pk>/', manager_detail_customer, name='manager-customer'),
    path('m/order/<int:pk>/', manager_order, name='manager-order'),
    path('m/selects/type-order/<int:pk>/', type_order_remove, name='selects-type_order-remove'),
    path('m/selects/format-order/<int:pk>/', format_order_remove, name='selects-format_order-remove'),
    path('m/selects/price-deadline-order/<int:pk>/', price_deadline_order_remove, name='selects-price_deadline-remove'),
    path('m/selects/', manager_selects, name='manager-selects'),
    path('m/settings/', manager_settings, name='manager-settings'),
    path('m/users/', manager_users, name='manager-users'),
    path('', DashboardViews.as_view(), name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
