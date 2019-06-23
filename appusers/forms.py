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
    select_user = forms.ChoiceField(
        choices=(('1', 'Writer'), ('2', 'Manager')),
        label='Select group',
        widget=forms.Select(attrs={'class': 'browser-default custom-select'})
    )

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
        },
