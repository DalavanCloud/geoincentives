from coffin.shortcuts import render_to_response as jinja2_render_to_response
#from geoincentives.forms import SignupForm

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from geoincentives.models import User

def home(request):

    context = {}
    context.update(csrf(request))

    return jinja2_render_to_response(
        'home.html', context
    )

@login_required(login_url='/login/')
def history(request):


    events = [] #request.user.get_nearby_events()

    return jinja2_render_to_response(
        'eventhistory.html', {
            'events': events,
        }
    )

@login_required(login_url='/login/')
def useraccount(request):


    return jinja2_render_to_response(
        'useraccount.html', {
            #'events': events,
        }
    )

@login_required(login_url='/login/')
def redemption(request):


    events = [] #request.user.get_nearby_events()

    return jinja2_render_to_response(
        'redemption.html', {
            'events': events,
        }
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
            form.save()
            return HttpResponseRedirect('/checkin/')

        print form.errors

    context['signup_form'] = SignupForm()

    return jinja2_render_to_response(
        'signup.html', context
    )
