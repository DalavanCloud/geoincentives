from coffin.shortcuts import render_to_response as jinja2_render_to_response
from geoincentives.forms import UserLoginForm, SignupForm
from django.http import HttpResponseRedirect
from geoincentives.models import User

def home(request):

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            try:
                User.objects.get(
                    email=form.cleaned_data['email'],
                    password= form.cleaned_data['password'],
                    # should encrypt password=User.hash_password(form.cleaned_data['password'])
                )
            except:
                return jinja2_render_to_response(
                    'home.html', {
                        'login_form': form
                    }
                )

            return HttpResponseRedirect('/user')


    return jinja2_render_to_response(
        'home.html', {
            'login_form': UserLoginForm()
        }
    )

def user(request):
    return jinja2_render_to_response(
        'user.html', {
        }
    )

def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/checkin')


    return jinja2_render_to_response(
        'signup.html', {
            'signup_form': SignupForm(),
            'login_form': UserLoginForm()
        }
    )
