from django import forms

from appcourses.models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            'title',
            'question',
            'pages',
            'description',
            'price_for_writer',
            'price_for_customer',
            'to_writer',
            'writer',
        ]