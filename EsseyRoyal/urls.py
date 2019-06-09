from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from appaaa.cron import search_deadline
from appaaa.sitemaps import ArticleSitemap, StaticViewSitemap
from appaaa.views import HomePageViews, feedback, calculate_home, order_feedback, add_comment
from apporders.ajax import chat_message_accept
from appusers.views import register, login_user

sitemaps = {
    'articles': ArticleSitemap,
    'static': StaticViewSitemap
}

admin.site.site_header = 'Панель управления'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', HomePageViews.as_view(), name='home'),
    path('cron/search-deadline/', search_deadline),
    path('accounts/login/', login_user, name='login'),
    path('add-comment/', add_comment, name='add-comment'),
    path('feedback/', feedback, name='feedback'),
    path('accounts/register/', register, name='register'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    # CUSTOMER
    path('order/', include('apporders.urls'), name='apporders'),

    path('dashboard/', include('appdashboard.urls'), name='appdashboard'),

    path('ajax/chat-message-accept/', chat_message_accept),
    path('ajax/calculate/', calculate_home),
    path('ajax/order-feedback/', order_feedback),
    path('blog/', include('appblog.urls', namespace='appblog')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
