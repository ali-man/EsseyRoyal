from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from EsseyRoyal.views import HomePageViews
from appdashboard.views import DashboardViews, admin_users, admin_selects, admin_settings
from apporders.views import ViewOrderViews, add_order_views, UpdateOrderViews, writer_order_detail, writer_order_review, \
    customer_order_in_progress
from appusers.views import change_profile

admin.site.site_header = 'Панель управления'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageViews.as_view(), name='home'),

    path('accounts/login/', LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True
    ), name='login'),

    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/change-profile', change_profile, name='change-profile'),

    # CUSTOMER
    path('orders/progress/<int:pk>/', customer_order_in_progress, name='customer-progress_order'),
    path('orders/view/<int:pk>/', ViewOrderViews.as_view(), name='view_order'),
    path('orders/update/<int:pk>/', UpdateOrderViews.as_view(), name='update_order'),
    path('order/new', add_order_views, name='add_order'),

    # WRITER
    path('dashboard/w/order/detail-<int:pk>/', writer_order_detail, name='writer-order_detail'),
    path('dashboard/w/order/review-<int:pk>/', writer_order_review, name='writer-order_review'),

    # ADMIN
    path('dashboard/users/', admin_users, name='admin-users'),
    path('dashboard/selects/', admin_selects, name='admin-selects'),
    path('dashboard/settings/', admin_settings, name='admin-settings'),
    path('dashboard/billing/', DashboardViews.as_view(), name='admin-billing'),

    path('dashboard/', DashboardViews.as_view(), name='dashboard'),

    # path('sign-up/', SignUpViews.as_view(), name='signup'),
    # path('sign-in/', SignInViews.as_view(), name='signin'),
    # path('logout/', logout_user, name='logout'),
    # path('dashboard/', dashboard_redirect, name='dashboard'),
    # path('blog/add-article/', add_article, name='blog-add_article'),
    # path('blog/add-tag/', add_tag, name='blog-add_tag'),
    # path('blog/<int:pk>-<str:slug>/', ArticleViews.as_view(), name='blog-detail'),
    # path('blog/', BlogViews.as_view(), name='blog'),
    # path('customer/order/view/<int:pk>/', ViewOrderViews.as_view(), name='customer_view_order'),
    # path('customer/order/add/', AddOrderViews.as_view(), name='customer_add_order'),
    # path('customer/', CustomerDashboardViews.as_view(), name='customer'),
    # path('manager/', ManagerDashboardViews.as_view(), name='manager'),
    # path('admin/manager/edit/<int:pk>/', EditManagerAdminDashboardViews.as_view(), name='admin-manager_edit'),
    # path('admin/managers/', ManagersAdminDashboardViews.as_view(), name='admin-managers'),
    # path('admin/writer/edit/<int:pk>/', EditWriterAdminDashboardViews.as_view(), name='admin-writer_edit'),
    # path('admin/writers/', WritersAdminDashboardViews.as_view(), name='admin-writers'),
    # path('admin/clients/', ClientsAdminDashboardViews.as_view(), name='admin-clients'),
    # path('admin/orders-review/', OrderReviewAdminDashboardViews.as_view(), name='admin-order_review'),
    # path('admin/orders/', OrderAdminDashboardViews.as_view(), name='admin-order'),
    # path('admin/', AdminDashboardViews.as_view(), name='admin'),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('api_auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
