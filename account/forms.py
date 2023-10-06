from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Account


from django.forms import ModelForm, TextInput, EmailInput

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'confirm_password']
        widgets = {
            'first_name': TextInput(attrs={'class': "form-control", 'placeholder': 'Enter Your Name' }),
            'last_name': TextInput(attrs={'class': "form-control", 'placeholder': 'Enter Your Last Name' }),
            'phone_number': TextInput(attrs={'class': "form-control",'placeholder': 'Enter Your Phone Number'}),
            'email': EmailInput(attrs={'class': "form-control", 'placeholder': 'Email'}),
        }

    # def __init__(self, *args, **kwargs):

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Passwords does not mutch!'
            )
        return super().clean()