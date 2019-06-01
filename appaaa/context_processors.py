from appblog.models import Article


def get_articles(val=None):
    articles = Article.objects.all()
    return {'articles': articles}