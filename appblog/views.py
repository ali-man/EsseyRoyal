from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from appblog.forms import TagForm, ArticleForm
from appblog.models import Article, Tag


class ListArticles(ListView):
    model = Article
    template_name = 'blog/main.html'


def article(request, article_id):
    item = get_object_or_404(Article, id=article_id)
    return render(request, 'blog/detail.html', {'article': item})


# class BlogViews(ListView):
#     model = Article
#     template_name = 'blog/list-articles.html'
#
#
class ArticleViews(DetailView):
    model = Article
    template_name = 'blog/detail.html'
#
#
# def add_tag(request):
#     form = TagForm()
#     if request.method == 'POST':
#         form = TagForm(request.POST)
#         if form.is_valid():
#             form.save()
#     return render(request, 'blog/add-tag.html', context={'form': form})
#
#
# def add_article(request):
#     form = ArticleForm()
#     if request.method == 'POST':
#         article = Article()
#         article.title = request.POST['title']
#         article.poster = request.FILES['poster']
#         article.description = request.POST['description']
#         if request.POST['status'] != 'on':
#             article.status = False
#         article.save()
#
#         tags = request.POST.getlist('list_tags', None)
#         if tags is not None:
#             for t in tags:
#                 try:
#                     tag_id = int(t)
#                     print(tag_id)
#                     tag = Tag.objects.get(id=tag_id)
#                     article.tags.add(tag)
#                 except ValueError:
#                     tag = Tag()
#                     tag.name = t
#                     tag.save()
#                     article.tags.add(tag)
#         return redirect('/blog/')
#
#     return render(request, 'blog/add-article.html', context={'form': form})
