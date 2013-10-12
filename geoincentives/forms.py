from django.forms import ModelForm
from geoincentives.models import User
from django import forms


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email', 'password'
        )
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control', }),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', })
        }
