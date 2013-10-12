from coffin.shortcuts import render_to_response as jinja2_render_to_response
from geoincentives.forms import SignupForm

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User as DjangoUser

from geoincentives.models import User

def home(request):

    context = {}
    context.update(csrf(request))

    return jinja2_render_to_response(
        'home.html', context
    )

@login_required(login_url='/login/')
def checkin(request):

    print request.session
    #from IPython import embed; embed()

    events = [] #request.user.get_nearby_events()

    return jinja2_render_to_response(
        'checkin.html', {
            'events': events,
        }
    )

@csrf_protect
def signup(request):
    context = {}
    context.update(csrf(request))

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            django_user = DjangoUser.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                form.cleaned_data['password'])

            django_user.first_name = form.cleaned_data['first_name']
            django_user.last_name = form.cleaned_data['last_name']
            django_user.save()

            user = User(
                auth_user=django_user,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode'],
                school=form.cleaned_data['school'],
                birthdate=form.cleaned_data['birthdate']
            )
            user.save()

            return HttpResponseRedirect('/checkin/')

        print form.errors

    context['signup_form'] = SignupForm()

    return jinja2_render_to_response(
        'signup.html', context
    )
