from django import forms

from appblog.models import Article, Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class ArticleForm(forms.ModelForm):

    list_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'browser-default custom-select js-example-basic-multiple',
                'multiple': 'multiple'
            }
        )
    )

    class Meta:
        model = Article
        fields = ['title', 'poster', 'description', 'status']
        widgets = {
            # 'tags': forms.Select(attrs={
            #     'class': 'browser-default custom-select js-example-basic-multiple',
            #     'multiple': 'multiple'
            # }),
            'status': forms.CheckboxInput(attrs={'style': 'opacity: 1;'})
        }