from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from appblog.forms import TagForm, ArticleForm
from appblog.models import Article, Tag
from appdashboard.views import access_to_manager_and_admin


class ListArticles(ListView):
    model = Article
    template_name = 'blog/main.html'

    def get_queryset(self):
        return Article.objects.all()[:5]

    def get_context_data(self, **kwargs):
        context = super(ListArticles, self).get_context_data(**kwargs)
        context['access_is_allowed'] = access_to_manager_and_admin(self.request.user)
        return context


def article(request, pk):
    item = get_object_or_404(Article, id=pk)
    return render(request, 'blog/detail.html', {'article': item})


class ArticleViews(DetailView):
    model = Article
    template_name = 'blog/detail.html'


def article_edit(request, pk):
    if not access_to_manager_and_admin(request.user):
        messages.error(request, 'Access is limited')
        return redirect('/dashboard/')
    article = Article.objects.get(id=pk)
    form = ArticleForm(instance=article)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article successfully updated')
            return redirect('/blog/')
    return render(request, 'blog/edit.html', context={'form': form, 'article': article})


def article_remove(request, pk):
    if not access_to_manager_and_admin(request.user):
        messages.error(request, 'Access is limited')
        return redirect('/dashboard/')
    article = Article.objects.get(id=pk)
    article.delete()
    messages.info(request, 'Article successfully deleted')
    return redirect('/blog/')