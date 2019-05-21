import datetime

from ckeditor.widgets import CKEditorWidget
from django import forms

from apporders.models import FormatOrder, TypeOrder, Order, PriceDeadline


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['status', 'per_page', 'total_cost', 'writer', 'customer']
        widgets = {
            'type_order': forms.Select(attrs={'class': 'browser-default custom-select'}),
            'format_order': forms.Select(attrs={'class': 'browser-default custom-select'}),
            'description': CKEditorWidget()
        }


class OrderAddForm(forms.Form):
    title = forms.CharField()
    type_order = forms.ModelChoiceField(queryset=TypeOrder.objects.all(), label='Type of order',
                                        widget=forms.Select(attrs={'class': 'browser-default custom-select'}))
    format_order = forms.ModelChoiceField(queryset=FormatOrder.objects.all(),
                                          widget=forms.Select(attrs={'class': 'browser-default custom-select'}))
    number_page = forms.IntegerField()
    date_deadline = forms.DateField(
        required=False, input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'class': 'browser-default custom-select',
                'id': 'date_deadline'
            }
        )
    )
    time_deadline = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            attrs={
                'type': 'text',
                'class': 'browser-default custom-select',
                'id': 'time_deadline'
            }
        )
    )
    # deadline_writer = forms.DateTimeField()
    # attached_files = forms.FileField(label='Files', widget=forms.ClearableFileInput(attrs={'multiple': True}))
    description = forms.CharField(widget=CKEditorWidget())

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
#     exclude = ['customer', 'created_datetime', 'status']
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


class TypeOrderForm(forms.ModelForm):
    class Meta:
        model = TypeOrder
        fields = '__all__'


class FormatOrderForm(forms.ModelForm):
    class Meta:
        model = FormatOrder
        fields = '__all__'


class PriceDeadlineForm(forms.ModelForm):
    class Meta:
        model = PriceDeadline
        fields = '__all__'