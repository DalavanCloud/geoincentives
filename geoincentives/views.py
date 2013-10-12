from coffin.shortcuts import render_to_response as jinja2_render_to_response
from geoincentives.forms import SignupForm

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User as DjangoUser

from geoincentives.models import User, Event

def home(request):

    context = {}
    context.update(csrf(request))
    context['request'] = request

    return jinja2_render_to_response(
        'home.html', context
    )

@login_required(login_url='/login/')
def history(request):

    events = [] #request.user.get_nearby_events()

    return jinja2_render_to_response(
        'eventhistory.html', {
            'events': events,
            'request': request
        }
    )

@login_required(login_url='/login/')
def useraccount(request):


    return jinja2_render_to_response(
        'useraccount.html', {
            'request': request
        }
    )

@login_required(login_url='/login/')
def redemption(request):


    events = [] #request.user.get_nearby_events()

    return jinja2_render_to_response(
        'redemption.html', {
            'events': events,
            'request': request
        }
    )

#-121.9227413 37.3768341

@login_required(login_url='/login/')
def checkin(request):

    cur_lng = float(-121.9227413)
    cur_lat = float(37.3768341)

    events = Event.objects.raw('select * from geoincentives_event where ((latitude - %(cur_lat)s) * (latitude - %(cur_lat)s)) + ((longitude - %(cur_lng)s * (longitude - %(cur_lng)s)) < 200)' % { 'cur_lat': cur_lat, 'cur_lng': cur_lng})
    #((cur_lat - 37.3768341) * (cur_lat - 37.3768341)) + ((cur_lng - -121.9227413 * (cur_lng - -121.9227413)) < 200)
    #from IPython import embed; embed()
  
    return jinja2_render_to_response(
        'checkin.html', {
            'events': events,
            'request': request
        }
    )

@csrf_protect
def signup(request, type=None):
    if not type:
        type = 1

    context = { 'request': request, 'type': type }
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
                type=type
            )

            if (form.cleaned_data['birthdate']):
                user['birthdate'] = form.cleaned_data['birthdate']

            user.save()

            return HttpResponseRedirect('/checkin/')

        print form.errors

    context['signup_form'] = SignupForm()

    return jinja2_render_to_response(
        'signup.html', context
    )
