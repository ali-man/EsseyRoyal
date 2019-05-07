import datetime

from ckeditor.widgets import CKEditorWidget
from django import forms

from apporders.models import Order, FormatOrder, DeadLine


class OrderAddForm(forms.Form):
    title = forms.CharField()
    type_order = forms.CharField()
    format_order = forms.ModelChoiceField(queryset=FormatOrder.objects.all(), widget=forms.Select(attrs={'class': 'browser-default custom-select'}))
    deadline = forms.ModelChoiceField(queryset=DeadLine.objects.all(), widget=forms.Select(attrs={'class': 'browser-default custom-select'}))
    date_deadline_writer = forms.DateField(
        required=False, input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'class': 'browser-default custom-select',
                'id': 'date_deadline_writer'
            }
        )
    )
    time_deadline_writer = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                'type': 'text',
                'class': 'browser-default custom-select',
                'id': 'time_deadline_writer'
            }
        )
    )
    # deadline_writer = forms.DateTimeField()
    # attached_files = forms.FileField(label='Files', widget=forms.ClearableFileInput(attrs={'multiple': True}))
    feedback = forms.CharField(widget=CKEditorWidget())


# class OrderForm(forms.ModelForm):
    # deadline_writer = forms.DateTimeField(
    #     required=False, input_formats=['%Y-%m-%dT%H:%M:%S+0000'],
    #     widget=forms.DateTimeInput(
    #         attrs={
    #             'type': 'datetime-local',
    #             'class': 'browser-default custom-select'
    #         })
    # )

    # class Meta:
    #     model = Order
    #     exclude = ['client', 'created_datetime', 'status']
    #     widgets = {
    #         'format_order': forms.Select(attrs={'class': 'browser-default custom-select'}),
    #         'deadline': forms.Select(attrs={'class': 'browser-default custom-select'}),
    #         'attached_files': forms.ClearableFileInput(attrs={'multiple': True}),
    #         'feedback': CKEditorWidget(),
    #         'deadline_writer': forms.DateTimeInput(
    #             attrs={
    #                 'class': 'browser-default custom-select'
    #             }
    #         )
    #     }
