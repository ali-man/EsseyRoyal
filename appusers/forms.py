from django import forms

from appusers.models import User


class UserCustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'academic_institution', 'degree', 'phone', 'avatar']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'academic_institution', 'degree', 'phone', 'avatar', 'corporate_email']


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password',
            'corporate_email', 'phone', 'academic_institution',
            'degree', 'avatar'
        ]
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
        }
