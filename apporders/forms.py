import datetime

from ckeditor.widgets import CKEditorWidget
from django import forms

from apporders.models import FormatOrder, TypeOrder, Order, PriceDeadline


class OrderForm(forms.ModelForm):
    date_deadline = forms.DateField(
        required=True, input_formats=['%d-%m-%Y'], label='Deadline',
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'class': 'browser-default custom-select',
                'id': 'date_deadline',
                'placeholder': 'Choose date',
                'autocomplete': 'off'
            }
        )
    )
    time_deadline = forms.TimeField(
        required=True, label='Deadline Time',
        widget=forms.TimeInput(
            attrs={
                'type': 'text',
                'class': 'browser-default custom-select',
                'id': 'time_deadline',
                'placeholder': 'Choose time',
                'autocomplete': 'off'
            }
        )
    )
    class Meta:
        model = Order
        exclude = ['status', 'per_page', 'total_cost', 'writer', 'customer', 'deadline']
        widgets = {
            'type_order': forms.Select(attrs={'class': 'browser-default custom-select'}),
            'format_order': forms.Select(attrs={'class': 'browser-default custom-select'}),
            'description': CKEditorWidget(),
        }


class OrderAddForm(forms.Form):
    BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Type a title...'}))
    type_order = forms.ModelChoiceField(queryset=TypeOrder.objects.all(), required=True, label='Type of order',
                                        widget=forms.Select(attrs={'class': 'browser-default custom-select'}))
    format_order = forms.ModelChoiceField(queryset=FormatOrder.objects.all(), required=True, label='Citation formatting',
                                          widget=forms.Select(attrs={'class': 'browser-default custom-select'}))
    # number_page = forms.IntegerField(required=True, label='Number of pages', widget=forms.NumberInput(
    #     attrs={
    #         'placeholder': 'Choose a number',
    #         'class': 'browser-default custom-select',
    #     }
    # ))
    _date = datetime.date.today() + datetime.timedelta(days=8)
    date_deadline = forms.DateField(
        required=True, input_formats=['%d-%m-%Y'], label='Deadline',
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'class': 'browser-default custom-select',
                'id': 'date_deadline',
                'placeholder': 'Choose date',
                'autocomplete': 'off'
            }
        )
    )
    time_deadline = forms.TimeField(
        required=True, label='Deadline Time',
        widget=forms.TimeInput(
            attrs={
                'type': 'text',
                'class': 'browser-default custom-select',
                'id': 'time_deadline',
                'placeholder': 'Choose time',
                'autocomplete': 'off'
            }
        )
    )
    number_page = forms.CharField(required=True, label='Number of pages', widget=forms.Select(
        attrs={
            'class': 'browser-default custom-select',
            'placeholder': 'Choose a number'
        }
    ))
    # deadline_writer = forms.DateTimeField()
    # attached_files = forms.FileField(label='Files', widget=forms.ClearableFileInput(attrs={'multiple': True}))
    description = forms.CharField(widget=CKEditorWidget(attrs={'placeholder': 'Describe your order in more detail...'}), required=False)

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