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

class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'password', 'email', 'first_name', 'last_name',
            'address', 'city', 'state', 'zipcode', 'school', 'birthdate'
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'zipcode': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'school': forms.TextInput(attrs={'placeholder': 'School', 'class': 'form-control GINGER_SOFATWARE_control', }),
            'birthdate': forms.TextInput(attrs={'placeholder': 'Birth Date', 'class': 'form-control GINGER_SOFATWARE_control', }),
        }





