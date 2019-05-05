from django.shortcuts import render
from django.views.generic.base import View


class HomePageViews(View):
    @staticmethod
    def get(request):

        return render(request, 'home.html', locals())