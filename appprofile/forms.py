from django import forms

from appprofile.models import Writer, Manager


class WriterForm(forms.ModelForm):

    class Meta:
        model = Writer
        exclude = ['user']


class ManagerForm(forms.ModelForm):

    class Meta:
        model = Manager
        exclude = ['user']