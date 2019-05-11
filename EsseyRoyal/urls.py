from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from EsseyRoyal.views import HomePageViews
from appdashboard.views import \
    CustomerDashboardViews, \
    OrderReviewAdminDashboardViews, \
    OrderAdminDashboardViews, \
    WritersAdminDashboardViews, \
    AdminDashboardViews, \
    dashboard_redirect, EditWriterAdminDashboardViews, ClientsAdminDashboardViews
from apporders.views import ViewOrderViews, AddOrderViews
from appusers.views import SignUpViews, SignInViews, logout_user

admin.site.site_header = 'Панель управления'
urlpatterns = [
    path('', HomePageViews.as_view(), name='home'),
    path('sign-up/', SignUpViews.as_view(), name='signup'),
    path('sign-in/', SignInViews.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', dashboard_redirect, name='dashboard'),
    path('customer/order/view/<int:pk>/', ViewOrderViews.as_view(), name='customer_view_order'),
    path('customer/order/add/', AddOrderViews.as_view(), name='customer_add_order'),
    path('customer/', CustomerDashboardViews.as_view(), name='customer'),
    path('admin/writer/edit/<int:pk>/', EditWriterAdminDashboardViews.as_view(), name='admin-writer_edit'),
    path('admin/writers/', WritersAdminDashboardViews.as_view(), name='admin-writers'),
    path('admin/clients/', ClientsAdminDashboardViews.as_view(), name='admin-clients'),
    path('admin/orders-review/', OrderReviewAdminDashboardViews.as_view(), name='admin-order_review'),
    path('admin/orders/', OrderAdminDashboardViews.as_view(), name='admin-order'),
    path('admin/', AdminDashboardViews.as_view(), name='admin'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api_auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
