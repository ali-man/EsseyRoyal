from django import forms

from appprofile.models import Writer


class WriterForm(forms.ModelForm):

    class Meta:
        model = Writer
        exclude = ['user']