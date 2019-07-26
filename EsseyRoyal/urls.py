from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import redirect
from django.urls import path, include

from appaaa.cron import search_deadline, check_order
from appaaa.sitemaps import ArticleSitemap, StaticViewSitemap
from appaaa.views import HomePageViews, feedback, calculate_home, order_feedback, add_testimonial, add_word
from apporders.ajax import chat_message_accept
from appusers.models import User
from appusers.views import register, login_user

sitemaps = {
    'articles': ArticleSitemap,
    'static': StaticViewSitemap
}


def redirect_dashboard(request):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user)
        group = [g for g in user.groups.all()]
        print(group)
        if len(group) != 0:
            group_name = group[0].name
            if group_name == 'Customer':
                return redirect('/c/orders/')
            if group_name == 'Writer':
                return redirect('/w/orders/')
            if group_name == 'Manager':
                return redirect('/m/orders/')
        else:
            return redirect('/a/')
    else:
        return redirect('/')


admin.site.site_header = 'Панель управления'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', HomePageViews.as_view(), name='home'),
    path('cron/search-deadline/', search_deadline),
    path('cron/check-orders/', check_order),
    path('accounts/login/', login_user, name='login'),
    path('add-comment/', add_testimonial, name='add-comment'),
    path('feedback/', feedback, name='feedback'),
    path('accounts/register/', register, name='register'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('rct/', redirect_dashboard),

    path('ajax/chat-message-accept/', chat_message_accept),
    path('ajax/calculate/', calculate_home),
    path('ajax/order-feedback/', order_feedback),
    path('ajax/add-word/', add_word),
    path('blog/', include('appblog.urls', namespace='appblog')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('c/', include('appdashboard.c', namespace='customer')),
    path('w/', include('appdashboard.w', namespace='writer')),
    path('m/', include('appdashboard.m', namespace='manager')),
    path('a/', include('appdashboard.a', namespace='administrator')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
