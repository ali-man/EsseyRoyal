from django.shortcuts import render
from django.views.generic.base import View

from appblog.models import Article


class HomePageViews(View):
    @staticmethod
    def get(request):
        articles = Article.objects.all()[:3]

        return render(request, 'home.html', locals())