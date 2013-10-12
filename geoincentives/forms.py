from django.forms import ModelForm
from geoincentives.models import User
from django import forms




class StudentLoginForm(forms.Form):
    username = forms.CharField(
        max_length=96,
        label='Username',
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'class': 'span5', 'required': ''}),
    )
    password = forms.CharField(
        max_length=255,
        label='Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'span5', }),
    )

class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    password = forms.CharField(
        max_length=100,
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    email = forms.CharField(
        max_length=255,
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    first_name = forms.CharField(
        max_length=128,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    last_name = forms.CharField(
        max_length=128,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    address = forms.CharField(
        max_length=255,
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    city = forms.CharField(
        max_length=255,
        label='City',
        widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    state = forms.CharField(
        max_length=30,
        label='State',
        widget=forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    zipcode = forms.CharField(
        max_length=5,
        label='Zip Code',
        widget=forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    school = forms.CharField(
        max_length=255,
        label='School',
        widget=forms.TextInput(attrs={'placeholder': 'School', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )
    birthdate = forms.CharField(
        max_length=100,
        label='Birth Date',
        widget=forms.DateInput(format="%m/%d/%y", attrs={'placeholder': 'Birth Date mm/dd/yyyy', 'class': 'form-control GINGER_SOFATWARE_control', }),
    )






