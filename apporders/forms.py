from django import forms

from apporders.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ['client', 'created_datetime']