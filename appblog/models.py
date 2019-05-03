from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag name', max_length=30, unique=True)
    slug = models.SlugField(verbose_name='URL', max_length=30, unique=True, blank=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(verbose_name='Title', max_length=100)
    slug = models.SlugField(verbose_name='URL', max_length=100, blank=True)
    poster = models.ImageField(verbose_name='Poster', upload_to="blog/posters/")
    description = RichTextUploadingField(verbose_name='Description')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', blank=True)
    status = models.BooleanField(verbose_name='Published ?', default=True)
    created_datetime = models.DateTimeField(verbose_name='Created datetime', auto_now_add=True)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
