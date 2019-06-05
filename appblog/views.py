from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from appblog.forms import TagForm, ArticleForm
from appblog.models import Article, Tag


class ListArticles(ListView):
    model = Article
    template_name = 'blog/main.html'


def article(request, pk):
    item = get_object_or_404(Article, id=pk)
    return render(request, 'blog/detail.html', {'article': item})


class ArticleViews(DetailView):
    model = Article
    template_name = 'blog/detail.html'