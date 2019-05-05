from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from EsseyRoyal.views import HomePageViews
from appusers.views import SignUpViews, SignInViews, logout_user

admin.site.site_header = 'Панель управления'
urlpatterns = [
    path('', HomePageViews.as_view(), name='home'),
    path('sign-up/', SignUpViews.as_view(), name='signup'),
    path('sign-in/', SignInViews.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', include('appdashboard.urls', namespace='appdashboard')),
    path('orders/', include('apporders.urls', namespace='apporders')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api_auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
