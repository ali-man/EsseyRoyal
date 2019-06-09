from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from appaaa.cron import search_deadline
from appaaa.sitemaps import ArticleSitemap, StaticViewSitemap
from appaaa.views import HomePageViews, feedback, calculate_home, order_feedback, add_comment
from appblog.views import ListArticles, article
from appdashboard.users.admin import *
from appdashboard.users.manager import *
from appdashboard.views import DashboardViews, others, feedback_view, comment_view
from apporders.ajax import chat_message_accept
from apporders.views import ViewOrderViews, add_order_views, UpdateOrderViews, writer_order_detail, writer_order_review, \
    customer_order_in_progress, manager_order, remove_order, type_order_remove, format_order_remove, \
    price_deadline_order_remove, completed_order, completed_order_feedback, customer_order_in_completed, \
    writer_order_completed
from appusers.views import change_profile, register, login_user

sitemaps = {
    'articles': ArticleSitemap,
    'static': StaticViewSitemap
}

admin.site.site_header = 'Панель управления'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', HomePageViews.as_view(), name='home'),

    # path('accounts/login/', LoginView.as_view(
    #     template_name="accounts/login.html",
    #     redirect_authenticated_user=True
    # ), name='login'),

    path('cron/search-deadline/', search_deadline),

    path('accounts/login/', login_user, name='login'),

    path('add-comment/', add_comment, name='add-comment'),
    path('feedback/', feedback, name='feedback'),

    path('accounts/register/', register, name='register'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/change-profile/', change_profile, name='change-profile'),

    # CUSTOMER
    path('orders/progress/<int:pk>/', customer_order_in_progress, name='customer-progress_order'),
    path('orders/completed/<int:pk>/', customer_order_in_completed, name='customer-completed_order'),
    path('orders/view/<int:pk>/', ViewOrderViews.as_view(), name='view_order'),
    path('orders/update/<int:pk>/', UpdateOrderViews.as_view(), name='update_order'),
    path('order/new', add_order_views, name='add_order'),
    path('order/remove', remove_order, name='remove'),
    path('order/completed/<int:pk>/', completed_order, name='completed'),
    path('order/completed/feedback/<int:pk>/', completed_order_feedback, name='completed-feedback'),

    # WRITER
    path('dashboard/w/order/completed-<int:pk>/', writer_order_completed, name='writer-order_completed'),
    path('dashboard/w/order/detail-<int:pk>/', writer_order_detail, name='writer-order_detail'),
    path('dashboard/w/order/review-<int:pk>/', writer_order_review, name='writer-order_review'),

    path('dashboard/others/feedback/<int:pk>/', feedback_view, name='feedback-view'),
    path('dashboard/others/comment/<int:pk>/', comment_view, name='comment-view'),
    path('dashboard/others/', others, name='others'),

    # ADMIN
    path('dashboard/writer/<int:pk>/', admin_detail_writer, name='admin-writer'),
    path('dashboard/customer/<int:pk>/', admin_detail_customer, name='admin-customer'),
    path('dashboard/manager/<int:pk>/', admin_detail_manager, name='admin-manager'),
    path('dashboard/users/', admin_users, name='admin-users'),
    path('dashboard/selects/', admin_selects, name='admin-selects'),
    path('dashboard/settings/', admin_settings, name='admin-settings'),
    path('dashboard/billing/', DashboardViews.as_view(), name='admin-billing'),

    # Manager
    path('dashboard/m/writer/<int:pk>/', manager_detail_writer, name='manager-writer'),
    path('dashboard/m/customer/<int:pk>/', manager_detail_customer, name='manager-customer'),
    path('dashboard/m/order/<int:pk>/', manager_order, name='manager-order'),
    path('dashboard/m/selects/type-order/<int:pk>/', type_order_remove, name='selects-type_order-remove'),
    path('dashboard/m/selects/format-order/<int:pk>/', format_order_remove, name='selects-format_order-remove'),
    path('dashboard/m/selects/price-deadline-order/<int:pk>/', price_deadline_order_remove, name='selects-price_deadline-remove'),
    path('dashboard/m/selects/', manager_selects, name='manager-selects'),
    path('dashboard/m/settings/', manager_settings, name='manager-settings'),
    path('dashboard/m/users/', manager_users, name='manager-users'),

    path('dashboard/', DashboardViews.as_view(), name='dashboard'),

    path('ajax/chat-message-accept/', chat_message_accept),
    path('ajax/calculate/', calculate_home),
    path('ajax/order-feedback/', order_feedback),

    # path('blog/', ListArticles.as_view(), name='blog-main'),
    # path('blog/<int:pk>/', article, name='blog-article'),

    # path('payments/', include('apppayment.urls', namespace='apppayment')),
    path('blog/', include('appblog.urls', namespace='appblog')),

    path('pages/', include('django.contrib.flatpages.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('api_auth/', include('rest_framework.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
