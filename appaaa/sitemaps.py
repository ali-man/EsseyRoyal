import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from appblog.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Article.objects.all()

    def location(self, obj):
        return F'/blog/{obj.id}-{obj.slug}/'

    def lastmod(self, obj):
        return obj.created_datetime


class StaticViewSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8

    static_links = [
        {'url': '/pages/about/', 'last_mod': datetime.datetime(2018, 8, 2, 0, 0)},
        {'url': '/pages/faq/', 'last_mod': datetime.datetime(2018, 8, 2, 0, 0)},
        {'url': '/pages/freelance-writer/', 'last_mod': datetime.datetime(2018, 8, 2, 0, 0)},
        {'url': '/pages/privacy-policy/', 'last_mod': datetime.datetime(2018, 8, 2, 0, 0)},
        {'url': '/pages/term/', 'last_mod': datetime.datetime(2018, 8, 2, 0, 0)},
    ]

    def items(self):
        return self.static_links

    def location(self, obj):
        return obj['url']

    def lastmod(self, obj):
        return obj['last_mod']